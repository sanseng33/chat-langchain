"""Main entrypoint for the app."""
import json
import logging
import pickle
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.templating import Jinja2Templates
from langchain.vectorstores import VectorStore

from callback import QuestionGenCallbackHandler, StreamingLLMCallbackHandler
from query_data import get_chain
from schemas import ChatResponse

from nlp import spectralCluster
from eureka import metadataDna

app = FastAPI()
templates = Jinja2Templates(directory="templates")
vectorstore: Optional[VectorStore] = None


@app.on_event("startup")
async def startup_event():
    logging.info("loading vectorstore")
    if not Path("vectorstore.pkl").exists():
        raise ValueError("vectorstore.pkl does not exist, please run ingest.py first")
    with open("vectorstore.pkl", "rb") as f:
        global vectorstore
        vectorstore = pickle.load(f)


@app.get("/")
async def get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    question_handler = QuestionGenCallbackHandler(websocket)
    stream_handler = StreamingLLMCallbackHandler(websocket)
    chat_history = []
    qa_chain = get_chain(vectorstore, question_handler, stream_handler)
    # Use the below line instead of the above line to enable tracing
    # Ensure `langchain-server` is running
    # qa_chain = get_chain(vectorstore, question_handler, stream_handler, tracing=True)

    while True:
        try:
            # Receive and send back the client message
            question = await websocket.receive_text()

            resp = ChatResponse(sender="you", message=question, type="stream")
            await websocket.send_json(resp.dict())

            # Construct a response
            start_resp = ChatResponse(sender="bot", message="", type="start")
            await websocket.send_json(start_resp.dict())

            meta = metadataDna(question)
            if len(meta) == 0:
                resp = ChatResponse(
                    sender="bot",
                    message="Sorry, something went wrong. Try again.",
                    type="error",
                )
                await websocket.send_json(resp.dict())
            phrases = []
            patent_phrases = {}
            patent_items = {}
            for item in meta:
                pitem = item['patent_id']
                fitem = item['tech_field']
                patent_items[pitem] = item
                phrases.append(fitem)
                if fitem not in patent_phrases:
                    patent_phrases[fitem] = [pitem]
                else:
                    patent_phrases[fitem].append(pitem)
            phrases = set(phrases)

            groupPhrase = spectralCluster(phrases, 'CN')

            resultBody = {}
            for phrases_in_cluster in groupPhrase:
                titleSpend = []
                for phrase in phrases_in_cluster:
                    patentIds = patent_phrases[phrase]
                    patentIds = set(patentIds)
                    for patentId in patentIds:
                        if len(titleSpend) < 20:
                            item = patent_items[patentId]
                            techTitle = item['tech_title']
                            titleSpend.append(techTitle)
                            titleSpend.append(".")

                message = ''.join(titleSpend)

                techFields = ','.join(phrases_in_cluster)

                resultBody['tech_fields'] = techFields
                resultBody['tech_solutions'] = message
                print(json.dumps(resultBody, ensure_ascii=False, encoding='utf-8'))

                result = await qa_chain.acall(
                    {"question": question, "chat_history": chat_history, "techFields": techFields}
                )
                # fieldResult= result["answer"]
                # await qa_chain.acall(
                #     {"question": question, "chat_history": chat_history, "techFields": fieldResult, "techSolutions": message}
                # )

            chat_history.append((question, result["answer"]))

            end_resp = ChatResponse(sender="bot", message="", type="end")
            await websocket.send_json(end_resp.dict())
        except WebSocketDisconnect:
            logging.info("websocket disconnect")
            break
        except Exception as e:
            logging.error(e)
            resp = ChatResponse(
                sender="bot",
                message="Sorry, something went wrong. Try again.",
                type="error",
            )
            await websocket.send_json(resp.dict())


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=9000)

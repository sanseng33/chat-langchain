from __future__ import unicode_literals

"""Main entrypoint for the app."""
import json
import os

from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from sklearn.cluster import KMeans

from nlp import spectralCluster
from schemas import ChatResponse
from typing import List, Dict, Union

from langchain.schema import Document
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
import numpy as np


app = FastAPI()
templates = Jinja2Templates(directory="templates")


class ChatQuery(BaseModel):
    patent_id: str = None
    tech_field: str = None
    tech_means: str = None
    tech_title: str = None
    pn: str = None


@app.post("/chat/group")
async def postChat(request: Dict[str, Union[List[ChatQuery], str]]):
    meta = []
    lang = ''
    if isinstance(request['data'], list):
        meta = request['data']
    if isinstance(request['lang'], str):
        lang = request['lang']

    if len(meta) == 0:
        resp = ChatResponse(
            sender="bot",
            message="Sorry, something went wrong. Try again.",
            type="error",
        )
        return resp.dict()
    phrases = []
    patent_phrases = {}
    patent_items = {}
    for item in meta:
        pitem = item.patent_id
        fitem = item.tech_field
        patent_items[pitem] = item
        phrases.append(fitem)
        if fitem not in patent_phrases:
            patent_phrases[fitem] = [pitem]
        else:
            patent_phrases[fitem].append(pitem)
    # phrases = set(phrases)

    groupPhrase = spectralCluster(phrases, lang)

    resultBody = []
    for phrases_in_cluster in groupPhrase:
        titleSpend = []
        resultItem = {}
        for phrase in phrases_in_cluster:
            patentIds = patent_phrases[phrase]
            patentIds = set(patentIds)
            for patentId in patentIds:
                if len(titleSpend) < 20:
                    item = patent_items[patentId]
                    techTitle = item.tech_title
                    titleSpend.append(techTitle)
                    titleSpend.append(".")

        message = ''.join(titleSpend)
        techFields = ','.join(phrases_in_cluster)

        resultItem['tech_fields'] = techFields
        resultItem['tech_solutions'] = message
        resultBody.append(resultItem)

    print(json.dumps(resultBody, ensure_ascii=False))

    return resultBody

@app.post("/chat/vectors")
async def postGroup(request: Dict[str, Union[List[ChatQuery], str]]):
    meta = []
    lang = ''
    if isinstance(request['data'], list):
        meta = request['data']
    if isinstance(request['lang'], str):
        lang = request['lang']

    if len(meta) == 0:
        resp = ChatResponse(
            sender="bot",
            message="Sorry, something went wrong. Try again.",
            type="error",
        )
        return resp.dict()
    phrases = []
    patent_phrases = {}
    patent_items = {}
    text = ''
    for item in meta:
        if item.tech_title is not None and item.tech_title != '':
            text = text + "Derived from patent " + item.pn + ":" + item.tech_title + " "
    vectorGroup(text)

def vectorGroup(text):

    text_splitter = RecursiveCharacterTextSplitter(separators=["\n\n", "\n", "\t"], chunk_size=1000, chunk_overlap=200)
    docs = text_splitter.create_documents([text])
    num_documents = len(docs)
    print(f"now is split up into {num_documents}")

    embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
    vectors = embeddings.embed_documents([x.page_content for x in docs])

    kmeans = KMeans(n_clusters=5, random_state=42).fit(vectors)

    kmeans_label = kmeans.labels_

    closest_indices = []
    for i in range(num_documents):
        distances = np.linalg.norm(vectors - kmeans_label.cluster_centers_[i], axis=1)
        closest_index = np.argmin(distances)
        closest_indices.append(closest_index)

    closest_indices = sorted(closest_indices)
    print(closest_indices)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=9000)

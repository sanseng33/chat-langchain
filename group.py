from __future__ import unicode_literals

"""Main entrypoint for the app."""
import json
import os
import nltk

from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from sklearn.cluster import KMeans

from nlp import spectralCluster
from schemas import ChatResponse
from typing import List, Dict, Union

from langchain.schema import Document
from langchain.embeddings import OpenAIEmbeddings
import numpy as np
import jieba


app = FastAPI()
templates = Jinja2Templates(directory="templates")


class ChatQuery(BaseModel):
    patent_id: str = None
    tech_field: str = None
    efficacy: str = None
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
    text = ''
    for item in meta:
        if item.tech_title is not None and item.tech_title != '':
            if lang == 'CN' or lang == 'cn':
                text += "来源于专利" + item.pn + ": 技术领域为"+ item.tech_field+"," + item.tech_title + "." + "达到效果:"+item.efficacy + "."
            else:
                text += "Derived from patent " + item.pn + ": technical field is "+ item.tech_field+"," + item.tech_title + "." + "achieve effect:"+item.efficacy + "."
    return vectorGroup(text, lang)

def vectorGroup(text, lang):
    if lang == "cn" or lang == "CN":
        text = " ".join(jieba.cut(text))
    docs = vecSplit(text)
    num_documents = len(docs)
    print(f"now is split up into {num_documents}")

    embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
    vectors = embeddings.embed_documents([x.page_content for x in docs])

    clusters = min(num_documents, 5)
    kmeans = KMeans(n_clusters=clusters, random_state=42).fit(vectors)
    kmeansl = kmeans.labels_

    closest_indices = []
    for i in range(clusters):
        distances = np.linalg.norm(vectors - kmeans.cluster_centers_[i], axis=1)
        closest_index = np.argmin(distances)
        closest_indices.append(closest_index)

    closest_indices = sorted(closest_indices)
    resultBody = []
    for index in closest_indices:
        resultItem = {}
        page = docs[index].page_content
        if lang == "cn" or lang == "CN":
            page.replace(" ", "")
        resultItem['tech_solutions'] = page
        resultBody.append(resultItem)
    return resultBody

def vecSplit(text):
    chunk_size = 400

    return create_document_list(text, chunk_size)

def split_text_into_chunks(text, chunk_size):
    tokens = nltk.word_tokenize(text)
    chunks = [tokens[i:i + chunk_size] for i in range(0, len(tokens), chunk_size)]
    return chunks

def create_document_list(text, chunk_size):
    nltk.download('punkt')  # Download the 'punkt' resource
    chunks = split_text_into_chunks(text, chunk_size)
    document_list = []
    for chunk in chunks:
        page_content = " ".join(chunk)
        document = Document(page_content=page_content)
        document_list.append(document)
    return document_list


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=9000)

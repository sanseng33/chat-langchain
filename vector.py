from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma

import numpy as np
import faiss

import os

def test():
    # Load the document, split it into chunks, embed each chunk and load it into the vector store.
    raw_documents = TextLoader('./state_of_the_union.txt').load()
    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=0)
    documents = text_splitter.split_documents(raw_documents)


    db = Chroma.from_documents(documents, OpenAIEmbeddings())

    query = "i want to see Patent Family, how to operate"
    docs = db.similarity_search(query)
    print(docs[0].page_content)

def faiss():
    raw_documents = TextLoader('./state_of_the_union.txt').load()
    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=0)
    documents = text_splitter.split_documents(raw_documents)
    embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
    vectors = embeddings.embed_documents([x.page_content for x in documents])
    d = vectors.shape[1]  # dimension of each vector
    np.random.seed(123)

    # 这将在内存中构建一个大小为 nb 的索引，向量的维度为 d
    index = faiss.IndexFlatL2(d)

    # 将向量添加到索引中
    index.add(vectors)



if __name__ == "__main__":

    # simpleChain()
    # simpleSequentialChain()
    # sequentialChain()
    test()
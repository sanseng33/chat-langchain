from langchain.agents import AgentType, initialize_agent
from langchain_community.chat_models import ChatOpenAI
from langchain_core.tools import Tool, StructuredTool
from langchain.tools import tool
from pydantic import BaseModel, Field
import requests, json
from langchain import LLMMathChain, SerpAPIWrapper

import os

os.environ["OPENAI_API_KEY"] = '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'


# 构建专利搜索
def PatentSearch(query: str) -> str:
    # Define the URL and the headers
    url = "http://localhost:8080/eureka/search/srp"
    headers = {
        'Content-Type': 'application/json',
        'X-API-Version': '1.0',
        'X-PatSnap-Version': 'v1',
        'X-User-ID': '73b511eef4104afda2fef37bcd94c100',
        'x-patsnap-from': 'w-analytics-patent-view',
        'x-site-lang': 'en'
    }

    # Define the payload
    payload = {
        "sort": "sdesc",
        "page": 1,
        "limit": 20,
        "novelty_id": "",
        "job_id": "",
        "q": query,
        "playbook": "SmartSearch",
        "_type": "query"
    }

    # Make the POST request and get the response
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    return response.text


tools = [Tool.from_function(func=PatentSearch, name='patent_search', description='在根据问题找相关专利时非常有用',
                            verbose=False)]

llm = ChatOpenAI(temperature=0.9, model_name='gpt-4')
agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

if __name__ == "__main__":
    resp = agent.run('锂电池的相关专利')
    print(resp)

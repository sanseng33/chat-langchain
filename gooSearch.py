import pprint

from googleapiclient.discovery import build

import os

os.environ["GOOGLE_CSE_ID"] = "d2d990dfd89ea4076"
os.environ["GOOGLE_API_KEY"] = "AIzaSyDe0T9OUYCs8x4aVsgAWMPSIvdX13UboZM"

from langchain.utilities import GoogleSearchAPIWrapper
os.environ["OPENAI_API_KEY"] = "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"

from langchain.utilities import GoogleSerperAPIWrapper
from langchain.llms.openai import OpenAI
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType

search = GoogleSearchAPIWrapper()

def top5_results(query):
    rs = search.results(query, 5)
    pprint.pprint(rs)
    return rs

tool = Tool(
    name="Google Search",
    description="Search Google for recent results.",
    func=top5_results,
)
tools = [
        Tool(
            name="Intermediate Answer",
            description="Search Google for recent results.",
            func=top5_results,
        )
    ]

llm = OpenAI(temperature=0.7)

self_ask_with_search = initialize_agent(
    tools, llm, agent=AgentType.SELF_ASK_WITH_SEARCH, verbose=True
)

def main():
    # Build a service object for interacting with the API. Visit
    # the Google APIs Console <http://code.google.com/apis/console>
    # to get an API key for your own application.
    service = build(
        "customsearch", "v1", developerKey="AIzaSyDe0T9OUYCs8x4aVsgAWMPSIvdX13UboZM"
    )

    res = (
        service.cse()
        .list(
            # q="HUAWEI lectures",
            q="Obama's first name?",
            cx="d2d990dfd89ea4076",
        )
        .execute()
    )

    pprint.pprint(res)


if __name__ == "__main__":
    # tool.run("如何提高锂电池能量密度?给出至多5中技术方案")
    self_ask_with_search.run("如何提高锂电池能量密度?给出至多5中技术方案")
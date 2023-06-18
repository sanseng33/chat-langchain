import os
import pprint

os.environ["SERPER_API_KEY"] = "029a8c451eb4053d1a7e67ef7719322c399d15c8"

from langchain.utilities import GoogleSerperAPIWrapper

search = GoogleSerperAPIWrapper()

search.run("Obama's first name?")

os.environ["OPENAI_API_KEY"] = "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"

from langchain.utilities import GoogleSerperAPIWrapper
from langchain.llms.openai import OpenAI
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType

llm = OpenAI(temperature=0.7)
search = GoogleSerperAPIWrapper()
tools = [
    Tool(
        name="Intermediate Answer",
        func=search.run,
        description="useful for when you need to ask with search",
    )
]

self_ask_with_search = initialize_agent(
    tools, llm, agent=AgentType.SELF_ASK_WITH_SEARCH, verbose=True
)


search = GoogleSerperAPIWrapper()
results = search.results("Apple Inc.")

if __name__ == "__main__":

    # pprint.pp(results)
    self_ask_with_search.run(
        # "What are the core technology directions of Huawei's research in recent years?"
        "如何提高锂电池能量密度?给出至多5中技术方案?"
    )
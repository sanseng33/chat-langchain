import os

os.environ["OPENAI_API_KEY"] = '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'
os.environ["TAVILY_API_KEY"] = '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'

from langchain_community.tools.tavily_search import TavilySearchResults

tools = [TavilySearchResults(max_results=1)]

from langgraph.prebuilt import ToolExecutor

tool_executor = ToolExecutor(tools)

from langchain.chat_models import ChatOpenAI

# We will set streaming=True so that we can stream tokens
# See the streaming section for more information on this.
model = ChatOpenAI(temperature=0, streaming=True)

from langchain.tools.render import format_tool_to_openai_function

functions = [format_tool_to_openai_function(t) for t in tools]
model = model.bind_functions(functions)

from typing import TypedDict, Annotated, Sequence
import operator
from langchain_core.messages import BaseMessage


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]

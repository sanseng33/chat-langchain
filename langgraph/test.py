from langchain_core.messages import HumanMessage
from graph import app


if __name__ == "__main__":
    inputs = {"messages": [HumanMessage(content="what is the weather in sf")]}
    print(app.invoke(inputs))
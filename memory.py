from langchain import ConversationChain
from langchain.memory import ConversationBufferMemory, ConversationSummaryBufferMemory, \
    ConversationBufferWindowMemory, ConversationTokenBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory, ConversationSummaryBufferMemory, \
    ConversationBufferWindowMemory, ConversationTokenBufferMemory
from langchain.prompts import PromptTemplate

template = """From now on, you are a professional python source code parsing expert.You can give an answer based on the question

{chat_history}
question: {human_input}
answer:"""

prompt = PromptTemplate(
    input_variables=["chat_history", "human_input"], template=template
)
memory = ConversationBufferMemory(memory_key="chat_history")


def conversationBufferMemory():
    llm = ChatOpenAI(temperature=0.0)
    memory = ConversationBufferMemory()
    conversation = ConversationChain(
        llm=llm,
        memory=memory,
        verbose=True
    )
    conversation.predict(input="Hi, my name is Andrew")

    conversation.predict(input="What is 1+1?")

    conversation.predict(input="What is my name?")

    print(memory.buffer)

    print(memory.load_memory_variables({}))
    memory.save_context({"input": "Hi"},
                        {"output": "What's up"})
    print(memory.load_memory_variables({}))


# 窗口
def conversationBufferWindowMemory():
    memory = ConversationBufferWindowMemory(k=1)

    memory.save_context({"input": "Hi"},
                        {"output": "What's up"})
    memory.save_context({"input": "Not much, just hanging"},
                        {"output": "Cool"})
    print(memory.load_memory_variables({}))

    llm = ChatOpenAI(temperature=0.0)
    conversation = ConversationChain(
        llm=llm,
        memory=memory,
        verbose=True
    )
    conversation.predict(input="Hi, my name is Andrew")

    conversation.predict(input="What is 1+1?")

    conversation.predict(input="What is my name?")

    print(memory.buffer)


def conversationTokenBufferMemory():
    llm = ChatOpenAI(temperature=0.0)
    memory = ConversationTokenBufferMemory(llm=llm, max_token_limit=30)

    memory.save_context({"input": "AI is what?!"},
                        {"output": "Amazing!"})

    memory.save_context({"input": "Backpropagation is what?"},
                        {"output": "Beautiful!"})

    memory.save_context({"input": "Chatbots are what?"},
                        {"output": "Charming!"})
    print(memory.load_memory_variables({}))


# 总结
def conversationSummaryBufferMemory():
    chat = ChatOpenAI(temperature=0.0)
    memory = ConversationSummaryBufferMemory(llm=chat, max_token_limit=800)
    chain = ConversationChain(
        llm=chat,
        memory=memory,
        verbose=True
    )
    # 以下是一篇小米公司的专利摘要，对这段摘要形成简单的总结：本公开提供一种切换控制方法及装置、存储介质，其中，所述方法包括：接收基站发送的无线资源控制RRC释放消息；在延迟时段内，停止条件重配过程以及对应的同步重配过程；其中，所述延迟时段是所述终端在接收到所述RRC释放消息后延迟进入非连接态的时段。或者，所述方法包括：接收基站发送的无线资源控制RRC释放消息；响应于在延迟时段内确定满足进行同步重配的重配条件，执行与所述重配条件对应的同步重配过程且停止RRC释放过程。本公开可以在终端接收到RRC释放消息后的延迟时段内避免同步重配过程失败，可用性高。
    response = chain.predict(
        input="以下是一篇华为公司的专利摘要，对这段摘要形成简单的总结：本申请实施例提供了一种通信的方法及相关设备。该方法包括：第一IAB宿主的CU确定F1接口应用协议(F1application protocol，F1AP)消息对应的QoS属性，其中，该F1接口为该第一IAB宿主的CU与IAB节点的DU之间的通信接口。之后，该第一IAB宿主的CU向第二IAB宿主的DU发送该F1AP消息和该F1AP消息对应的QoS属性。通过本方法，即使在第一IAB宿主的DU无法转发来自第一IAB宿主的CU的F1AP消息的情况下，也可以保证F1AP消息的传输。")
    print(response)

    # 查看历史存储记录
    response = memory.load_memory_variables({})
    print(response)

    response = chain.predict(
        input="以下是一篇小米公司的专利摘要，对这段摘要形成简单的总结：本公开提供一种切换控制方法及装置、存储介质，其中，所述方法包括：接收基站发送的无线资源控制RRC释放消息；在延迟时段内，停止条件重配过程以及对应的同步重配过程；其中，所述延迟时段是所述终端在接收到所述RRC释放消息后延迟进入非连接态的时段。或者，所述方法包括：接收基站发送的无线资源控制RRC释放消息；响应于在延迟时段内确定满足进行同步重配的重配条件，执行与所述重配条件对应的同步重配过程且停止RRC释放过程。本公开可以在终端接收到RRC释放消息后的延迟时段内避免同步重配过程失败，可用性高")
    print(response)

    # 查看历史存储记录
    response = memory.load_memory_variables({})
    print(response)

    response = chain.predict(
        input="以下是一篇华为公司的专利摘要，对这段摘要形成简单的总结：本申请提供了一种封装结构和封装结构的制作方法。该封装结构包括：第一电子元件、导电通道、第一导电结构、第二导电结构；导电通道贯穿第一电子元件；第一导电结构设于导电通道的底部；第二导电结构通过第一导电结构与导电通道电连接；在预设温度下第一导电结构的材料扩散能力低于第二导电结构的材料扩散能力。通过将退火温度等预设温度下扩散能力较弱的第一导电结构设置在导电通道的底部，使得在形成导电通道过程中采用的过刻蚀工艺导致引起的反溅射对第一电子元件电学性能的影响减小。")
    print(response)

    # 查看历史存储记录
    response = memory.load_memory_variables({})
    print(response)

    response = chain.predict(input="对以上提到的所有的华为公司的专利摘要进行简要总结")
    print(response)

    # 查看历史存储记录
    response = memory.load_memory_variables({})
    print(response)


def checkMemory():
    chat = ChatOpenAI(temperature=0.0)
    memory = ConversationSummaryBufferMemory(llm=chat, max_token_limit=1000)
    response = memory.load_memory_variables({})
    print(response)


if __name__ == "__main__":
    # conversationBufferMemory()

    # conversationBufferWindowMemory()

    # conversationTokenBufferMemory()

    conversationSummaryBufferMemory()

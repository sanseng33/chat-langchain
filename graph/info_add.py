# 设置OpenAI API密钥
import os

from langchain.chains import LLMChain
from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, \
    ChatPromptTemplate, PromptTemplate, AIMessagePromptTemplate

from graph.info_add_parser import InfoListOutputParser

os.environ["OPENAI_API_KEY"] = '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'

model = ChatOpenAI(model_name='gpt-4')

template = "请扮演一个行业的研发专家，帮我一起解决方案设计问题。"

output_parser = InfoListOutputParser()

system_message_prompt = SystemMessagePromptTemplate.from_template(template)

example_human = HumanMessagePromptTemplate.from_template(
    "现在需要设计一个内窥镜的压力反馈装置，完成这个设计还需要哪些维度的信息，以及他们的示例有哪些?信息最少输出3个，最多输出5个")

example_ai = AIMessagePromptTemplate.from_template(
    "目的:改善导航,增加生物组织的触感反馈,辅助手术操作;力反馈的类型和范围:触觉反馈,压力反馈,振动反馈;材料和兼容性:生物相容,防水,兼容消毒")
human_template = """{topic}的设计需要的信息有哪些? \n{format_instructions}"""
prompt = PromptTemplate(template=human_template, input_variables=['topic'],
                        partial_variables={"format_instructions": output_parser.get_format_instructions()})


def infoAdd(topic: str) -> str:
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, example_human, example_ai, prompt.format(topic=topic)]
    )
    chain = LLMChain(llm=model, prompt=chat_prompt, verbose=True)

    pt = chain.run(topic=topic)
    return output_parser.parse(pt)


if __name__ == "__main__":
    print(infoAdd('烘干机'))

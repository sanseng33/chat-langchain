# 设置OpenAI API密钥
import os

from langchain.chains import LLMChain, SimpleSequentialChain
from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, \
    ChatPromptTemplate, PromptTemplate, AIMessagePromptTemplate

os.environ["OPENAI_API_KEY"] = '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'

model = ChatOpenAI(model_name='gpt-4')

format_instructions = {
    "expected_format": "key1:[item1,item2];key2:[item3,item4]"
}

template = "请扮演一个行业的研发专家，帮我一起解决方案设计问题。"
system_message_prompt = SystemMessagePromptTemplate.from_template(template, input_args=['topic'])
example_human = HumanMessagePromptTemplate.from_template(
    "现在需要设计一个内窥镜的压力反馈装置，完成这个设计还需要哪些维度的信息，以及他们的示例有哪些?信息最少输出3个，最多输出5个")
example_ai = AIMessagePromptTemplate.from_template(
    "目的:[改善导航,增加生物组织的触感反馈,辅助手术操作];力反馈的类型和范围:[触觉反馈,压力反馈,振动反馈];材料和兼容性:[生物相容,防水,兼容消毒]")
human_template = "{topic}的设计需要的信息及它们的示例维度是什么?要求输出格式为：key1:[item1,item2];key2:[item3,item4]"
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template, input_args=['topic'])

chat_prompt = ChatPromptTemplate.from_messages(
    [system_message_prompt, example_human, example_ai, human_message_prompt]
)
chain = LLMChain(llm=model, prompt=chat_prompt, verbose=True)

pt = chain.run("烘干机")

print(pt)


# 定义自定义的解析函数
def custom_output_parser(response_text):
    output_dict = {}
    parts = response_text.split(";")
    for part in parts:
        key, value_str = part.split(":")
        value_list = value_str.strip("[]").split(",")
        output_dict[key] = value_list
    return output_dict


# 使用自定义的output_parser解析模型的响应
parsed_response = custom_output_parser(pt)
print(parsed_response)

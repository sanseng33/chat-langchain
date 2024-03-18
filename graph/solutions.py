import json
from typing import List, Dict

from langchain.chains import LLMChain
from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from pydantic.v1 import BaseModel, Field
import os

from graph.info_add import infoAdd
from graph.intent import textFix

os.environ["OPENAI_API_KEY"] = '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'

llm = ChatOpenAI(temperature=0.9, model_name='gpt-4')

# demo
# 请扮演一个研发专家，帮我一起解决问题
# 现在需要设计一个烘干机，
# 以下是一些设计要求信息：
# 1. 能效要求是节能、环保
# 2. 噪音控制是减震设计
# 3. 烘干能力是均匀烘干
# 请基于这些信息，并利用你知道的研发创新理论知识，给我 5 个方案并预测这些方案能达到的性能指标，并同时告诉我这 5 个方案是否有已有的具体应用案例，比如用在哪些现有的产品上的，具体到是哪家公司的哪个产品。
template = '现在需要设计{topic}\n以下是一些设计要求信息：{infos}\n请基于这些信息，并利用你知道的研发创新理论知识，给我 5 个方案并预测这些方案能达到的性能指标，并同时告诉我这 5 个方案是否有已有的具体应用案例，比如用在哪些现有的产品上的，具体到是哪家公司的哪个产品。\n{format_instructions}'


class Solution(BaseModel):
    solution_description: str = Field(description="方案描述")
    performance: str = Field(description="预期性能指标")
    case: str = Field(description="应用案例")


# 创建输出解析器
from langchain.output_parsers import PydanticOutputParser

output_parser = PydanticOutputParser(pydantic_object=Solution)

# 根据模板创建提示，同时在提示中加入输出解析器的说明
prompt = PromptTemplate.from_template(
    template,
    input_args=['topic', 'infos'],
    partial_variables={"format_instructions": output_parser.get_format_instructions()})

model = LLMChain(llm=llm, prompt=prompt, verbose=True)


def getSolution(topic: str, infos: dict) -> Solution:
    result = ";".join([f"{key}:{value}" for key, value in infos.items()])

    return model.run(topic=topic, infos=result)


if __name__ == "__main__":
    question = "树脂材料容易因为高温环境损坏，如何解决"
    resp = textFix(question)
    print(resp)
    jstr = json.loads(resp)
    word = jstr["extension"][0]

    infos = infoAdd(word)
    print(infos)

    infoStr = json.loads(infos)
    converted_dict = {key: value[0] for key, value in infoStr.items()}
    print(getSolution(word, converted_dict))


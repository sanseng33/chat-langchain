from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from pydantic.v1 import BaseModel, Field
import os

os.environ["OPENAI_API_KEY"] = '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'

model = LLMChain(model_name='gpt-4')

# demo
# 请扮演一个研发专家，帮我一起解决问题
# 现在需要设计一个烘干机，
# 以下是一些设计要求信息：
# 1. 能效要求是节能、环保
# 2. 噪音控制是减震设计
# 3. 烘干能力是均匀烘干
# 请基于这些信息，并利用你知道的研发创新理论知识，给我 5 个方案并预测这些方案能达到的性能指标，并同时告诉我这 5 个方案是否有已有的具体应用案例，比如用在哪些现有的产品上的，具体到是哪家公司的哪个产品。
template = '现在需要设计{topic}\n以下是一些设计要求信息：{infos}\n请基于这些信息，并利用你知道的研发创新理论知识，给我 5 个方案并预测这些方案能达到的性能指标，并同时告诉我这 5 个方案是否有已有的具体应用案例，比如用在哪些现有的产品上的，具体到是哪家公司的哪个产品。{format_instructions}'


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

pv = prompt.format(topic='烘干机', infos='1. 能效要求是节能、环保\n2. 噪音控制是减震设计\n3. 烘干能力是均匀烘干')

print(model.run(pv))

import os

from langchain.chains import LLMChain
from langchain_community.chat_models import ChatOpenAI
from pydantic.v1 import BaseModel, Field

os.environ["OPENAI_API_KEY"] = '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'

samples = """[
    {{
        \"question\": \"家用烘干机\",
        \"question_type\": \"单个技术主题\",
        \"question_code\": 1,
        \"extension\": \"[家用烘干机]\"
    }},
    {{
        \"question\": \"锂电池和磷酸铁锂电池的区别\",
        \"question_type\": \"多个技术主题\",
        \"question_code\": 2,
        \"extension\": \"[锂电池,磷酸铁锂电池]\"
    }},
    {{
        \"question\": \"提高家用烘干机的功率\",
        \"question_type\": \"技术问题\",
        \"question_code\": 3,
        \"extension\": \"[提高家用烘干机的功率]\"
    }},
    {{
        \"question\": \"锂电池存在一些充电功率问题，充电时间长\",
        \"question_type\": \"提取技术问题\",
        \"question_code\": 4,
        \"extension\": \"[提高锂电池充电功率,缩短锂电池充电时间]\"
    }},
    {{
        \"question\": \"最著名的艺术家有哪些\",
        \"question_type\": \"非技术描述\",
        \"question_code\": 5,
        \"extension\": \"[最著名的艺术家有哪些]\"
    }}
]"""

# 2. 创建一个提示模板
from langchain.prompts.prompt import PromptTemplate


class OutQuestionType(BaseModel):
    question_type: str = Field(description="问题类型")
    question_code: str = Field(description="问题代码")
    extension: list = Field(description="扩展")


# 创建输出解析器
from langchain.output_parsers import PydanticOutputParser

output_parser = PydanticOutputParser(pydantic_object=OutQuestionType)


def textFix(question: str) -> str:

    template = '请扮演一个行业的研发专家，帮我一起解决方案设计问题 \n根据不同问题区分的示例如下：{samples} \n现在一个新的问题是：{question} \n输出问题类型、问题代码和扩展。\n{format_instructions}'
    ht = PromptTemplate.from_template(template=template, input_args=['samples', 'question'],
                                      partial_variables={
                                          "format_instructions": output_parser.get_format_instructions()})


    print(ht)

    llm = ChatOpenAI(model_name="gpt-4", temperature=0)
    chain = LLMChain(llm=llm, prompt=ht, verbose=True)

    pt = chain.run(question=question, samples=samples)

    return pt


if __name__ == "__main__":
    question = "新能源汽车和油电混合汽车的理论"
    resp = textFix(question)
    print(resp)

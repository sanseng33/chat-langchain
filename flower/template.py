import os

os.environ["OPENAI_API_KEY"] = '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'

from langchain.vectorstores import Qdrant
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.prompts import FewShotPromptTemplate
from langchain.prompts import SystemMessagePromptTemplate
from langchain.prompts import HumanMessagePromptTemplate
from langchain.prompts import ChatPromptTemplate
from langchain.prompts.example_selector import SemanticSimilarityExampleSelector

# 1. 创建一些示例
samples = [
    {
        "flower_type": "玫瑰",
        "occasion": "爱情",
        "ad_copy": "玫瑰，浪漫的象征，是你向心爱的人表达爱意的最佳选择。"
    },
    {
        "flower_type": "康乃馨",
        "occasion": "母亲节",
        "ad_copy": "康乃馨代表着母爱的纯洁与伟大，是母亲节赠送给母亲的完美礼物。"
    },
    {
        "flower_type": "百合",
        "occasion": "庆祝",
        "ad_copy": "百合象征着纯洁与高雅，是你庆祝特殊时刻的理想选择。"
    },
    {
        "flower_type": "向日葵",
        "occasion": "鼓励",
        "ad_copy": "向日葵象征着坚韧和乐观，是你鼓励亲朋好友的最好方式。"
    }
]

exampleSelector = SemanticSimilarityExampleSelector.from_examples(
    samples,
    OpenAIEmbeddings(),
    Chroma,
    k=1
)

# 2. 创建一个提示模板
from langchain.prompts.prompt import PromptTemplate

template = "鲜花类型: {flower_type}\n场合: {occasion}\n文案: {ad_copy}"
prompt_sample = PromptTemplate(input_variables=["flower_type", "occasion", "ad_copy"],
                               template=template)

fewPrompt = FewShotPromptTemplate(
    example_selector=exampleSelector,
    example_prompt=prompt_sample,
    suffix="鲜花: {flower_type}\n场合: {occasion}",
    input_variables=["flower_type", "occasion"]
)

from langchain.chat_models import ChatOpenAI  # ChatOpenAI模型

llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

if __name__ == "__main__":

    print(fewPrompt.format(flower_type="黑玫瑰", occasion="忠贞"))
    ht = HumanMessagePromptTemplate.from_template("{flower_type}的宣传文案是？")
    prompt_template = ChatPromptTemplate.from_messages([st, fewPrompt.format(flower_type="黑玫瑰", occasion="忠贞"), ht])
    pt = prompt_template.format_prompt(flower_type="黑玫瑰").to_messages()
    print(pt)
    print(llm(pt))


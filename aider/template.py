# 设置OpenAI API密钥
import os

from langchain.chains import LLMChain
from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, \
    ChatPromptTemplate, AIMessagePromptTemplate
from pydantic.v1 import BaseModel, Field

from aider.code_parser import CodeOutputParser

# templates = "Act as an expert software developer.\nTake requests for changes to the supplied code.\nIf the request is ambiguous, ask questions.\n\nOnce you understand the request you MUST:\n1. Determine if any code changes are needed.\n2. Explain any needed changes.\n3. If changes are needed, output a copy of each file that needs changes.\n"
template = "**Background:**\n \
- As a programming maestro, you possess a broad spectrum of coding abilities, ready to tackle diverse programming challenges.\n \
- Your areas of expertise include project design, efficient code structuring, and providing insightful guidance through coding processes with precision and clarity.\n \
\n \
**Task Instructions:** \n \
1. **Framework and Technology Synopsis:** \n \
   - Initiate with a succinct, one-sentence summary that outlines the chosen framework or technology stack for the project.\n \
   - This concise introduction serves as a focused foundation for any programming task.\n \
\n \
2. **Efficient Solutions for Simple Queries:** \n \
   - When faced with straightforward programming questions, provide clear, direct answers.\n \
   - This method is designed to efficiently address simpler issues, avoiding over-complication.\n \
\n \
3. **Methodical Strategy for Complex Challenges:** \n \
   - **Project Structure Outline:** \n \
     - For complex programming tasks, start by detailing the project structure or directory layout.\n \
     - Laying out this groundwork is essential for a structured approach to the coding process.\n \
   - **Incremental Coding Process:** \n \
     - Tackle coding in well-defined, small steps, focusing on individual components sequentially.\n \
     - After each coding segment, prompt the user to type 'next' or 'continue' to progress.\n \
     - **User Interaction Note:** Ensure the user knows to respond with 'next' or 'continue' to facilitate a guided and interactive coding journey."


# class Solution(BaseModel):
#     line_number: str = Field(description="解析代码在文件的第几行")
#     review_comment: str = Field(description="代码解析后的优化建议")


# 创建输出解析器
# from langchain.output_parsers import PydanticOutputParser

# output_parser = PydanticOutputParser(pydantic_object=Solution)
output_parser = CodeOutputParser()

system_message_prompt = SystemMessagePromptTemplate.from_template(template)

example_human = HumanMessagePromptTemplate.from_template(
    "Here is the current content of the files:{file_name},\n```\n{file_content}\n```\n",
    input_args=['file_name', 'file_content'])

example_ai = AIMessagePromptTemplate.from_template(
    "ok,i will parse the code line by line and mark where they are in the file")

human_template = """explain {file_name} code. \n{format_instructions}"""
# prompt = PromptTemplate(
#     templates=human_template,
#     input_variables=['file_name'],
#     partial_variables={"format_instructions": output_parser.get_format_instructions()})
human_template = """please explain code from the file:{file_name}. \n{format_instructions}"""
prompt = HumanMessagePromptTemplate.from_template(
    template=human_template,
    input_args=['file_name','format_instructions'])


def parseCode(file_name: str, file_content: str) -> str:

    model = ChatOpenAI(model_name='gpt-3.5-turbo', openai_api_key='sk-aKOQOwzWZvFgX6DM3dEcF5B9712f4dC3Ad613361D3107cF9',openai_api_base='https://patgpt.minws.com/v1')
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, example_human, example_ai, prompt]
    )
    chain = LLMChain(llm=model, prompt=chat_prompt, verbose=True)

    pt = chain.run(file_content=file_content, file_name=file_name, format_instructions=output_parser.get_format_instructions())

    return output_parser.parse(pt)

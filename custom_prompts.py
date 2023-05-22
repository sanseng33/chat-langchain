# flake8: noqa
from langchain.prompts.prompt import PromptTemplate

prompt_field = """From now on you are a patent researcher, you can extract from a batch of technical domain words what the core technical domain is, only allowed to output one technical domains, no redundant answers, no explanatory answers.

technical domain words:

{context}"""
FIELD_PROMPT = PromptTemplate(
    template=prompt_field, input_variables=["context"]
)




prompt_solutions = """From now on you are a patent researcher, you can come up with one or two technical solutions based on a few technical solutions, and one technical areas. For example, given 10 technical solutions and one technical areas, you should export one or two technical solutions for the above technical areas. Keep it short, describing it in one or two sentences. No extra answers, no explanatory answers..

technical solutions:

{context}

technical areas:

{techFields}"""

SOLUTION_PROMPT = PromptTemplate(
    template=prompt_solutions, input_variables=["context", "techFields"]
)

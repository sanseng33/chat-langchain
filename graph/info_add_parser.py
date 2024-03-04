from langchain_core.exceptions import OutputParserException
from langchain_core.output_parsers import BaseOutputParser
from typing import Any
import re

CUSTOM_CODE_BLOCK_INSTRUCTIONS = """The output should be formatted as a JSON instance. \n \
As an example, for the output` key1:demo1,demo2,demo3;key2:demo4,demo5`,the json [{{\"key1\": [\"demo1\", \"demo2\", \"demo3\"]}},{{\"key2\": [\"demo4\", \"demo5\"]}}] is a well-formatted instance of the output\n  \
Here is the output:\n   \
```\n  \
(some content)\n  \
```"""


class InfoListOutputParser(BaseOutputParser):
    """
        自定义一个代码块输出解析器，继承BaseOutputParser类，其中的泛型表示解析后要返回的数据类型。
        继承基类后，需要实现3个方法，分别是：
        parse -> 该方法用于解析大模型的输出，将其解析为既定格式，返回值即为泛型类型，例如在列表解析中返回类型为List
        get_format_instructions -> 该方法返回一段提示词，该提示词需要嵌入到原本的提示词模板中，作为对大模型返回格式的提示
        _type -> 这是一个只读的私有方法，调用该方法可获取解析器的类型，类型支持自命名
    """
    # 自定义的一个字段，用于指定返回代码块的类型
    code_type: str = None

    # 在这段初始化方法中，指定了code_type只能为限定类型的代码
    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)

    def parse(self, text: str) -> str:
        """该方法用于解析模型的输出"""
        # 使用非贪婪匹配 .*? 来捕获三个反引号之间的任何内容
        pattern = r'\[.*\]'

        # 执行搜索
        match = re.search(pattern, text, re.DOTALL)

        # 判断并输出结果
        if match:
            code = match.group(1)
            return code
        else:
            raise OutputParserException("The response has no code block.", llm_output=text)

    def get_format_instructions(self) -> str:
        """给出格式化指令"""
        return CUSTOM_CODE_BLOCK_INSTRUCTIONS

    @property
    def _type(self) -> str:
        """返回该解析器的类型 这里返回的是自定义代码块解析器"""
        return "CustomCodeBlock"

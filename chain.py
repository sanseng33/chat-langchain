from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, StringPromptTemplate
from langchain.chains import LLMChain

from langchain.chains import SimpleSequentialChain
from langchain.chains import SequentialChain

from langchain.chains.router import MultiPromptChain
from langchain.chains.router.llm_router import LLMRouterChain,RouterOutputParser
from langchain.prompts import PromptTemplate

#简单链
def simpleChain():
    llm = ChatOpenAI(temperature=0.9)

    prompt = ChatPromptTemplate.from_template(
        "What is the best name to describe \
        a company that does {product}?"
    )

    chain = LLMChain(llm=llm, prompt=prompt)

    product = "Patent search database"
    print(chain.run(product))

#串行链
def simpleSequentialChain():
    llm = ChatOpenAI(temperature=0.9, model_name='gpt-4')

    # prompt template 1
    first_prompt = ChatPromptTemplate.from_template(
        "What is the best name to describe \
        a company that does {product}?"
    )

    # Chain 1
    chain_one = LLMChain(llm=llm, prompt=first_prompt)

    # prompt template 2
    second_prompt = ChatPromptTemplate.from_template(
        "Write a 20 words description for the following \
        company:{company_name}"
    )
    # chain 2
    chain_two = LLMChain(llm=llm, prompt=second_prompt)

    overall_simple_chain = SimpleSequentialChain(chains=[chain_one, chain_two],
                                                 verbose=True
                                                 )
    product = "Patent search databases"
    overall_simple_chain.run(product)

#并行链
def sequentialChain():
    llm = ChatOpenAI(temperature=0.9)

    # prompt template 1: translate to english
    first_prompt = ChatPromptTemplate.from_template(
        "Translate the following solution to english:"
        "\n\n{Solution}"
    )
    # chain 1: input= Solution and output= English_Solution
    chain_one = LLMChain(llm=llm, prompt=first_prompt,
                         output_key="English_Solution"
                         )

    # prompt template 2
    second_prompt = ChatPromptTemplate.from_template(
        "Can you summarize the following solution in 1 sentence:"
        "\n\n{English_Solution}"
    )
    # chain 2: input= English_Solution and output= summary
    chain_two = LLMChain(llm=llm, prompt=second_prompt,
                         output_key="summary"
                         )

    # prompt template 3: translate to english
    third_prompt = ChatPromptTemplate.from_template(
        "What language is the following solution:\n\n{Solution}"
    )
    # chain 3: input= Review and output= language
    chain_three = LLMChain(llm=llm, prompt=third_prompt,
                           output_key="language"
                           )

    # prompt template 4: follow up message
    fourth_prompt = ChatPromptTemplate.from_template(
        "Write a follow up response to the following "
        "summary in the specified language:"
        "\n\nSummary: {summary}\n\nLanguage: {language}"
    )
    # chain 4: input= summary, language and output= followup_message
    chain_four = LLMChain(llm=llm, prompt=fourth_prompt,
                          output_key="followup_message"
                          )

    # overall_chain: input= Review
    # and output= English_Review,summary, followup_message
    overall_chain = SequentialChain(
        chains=[chain_one, chain_two, chain_three, chain_four],
        input_variables=["Solution"],
        output_variables=["English_Solution", "summary", "followup_message"],
        verbose=True
    )

    solution='本申请实施例提供了一种芯片封装和芯片封装的制备方法，有利于提高芯片的性能。该芯片封装包括基板、裸芯片、第一保护结构和阻隔结构；该裸芯片、该第一保护结构和该阻隔结构均被设置在该基板的第一表面上；该第一保护结构包裹该裸芯片的侧面，该阻隔结构包裹该第一保护结构背离该裸芯片的表面，且该裸芯片的第一表面、该第一保护结构的第一表面和该阻隔结构的第一表面齐平，其中，该裸芯片的第一表面为该裸芯片背离该基板的表面，该第一保护结构的第一表面为该第一保护结构背离该基板的表面，该阻隔结构的第一表面为该阻隔结构背离该基板的表面。'
    response = overall_chain(solution)
    print(response)


def routerChain():

    physics_template = """你是一位非常聪明的物理学教授。
    你非常擅长用简洁的语言总结专利的物理学技术要点并回答物理问题。
    当你不知道问题的答案时，你需要回答你不知道。

    这里有一个问题:
    {input}"""

    math_template = """你是一个很好的数学家。
    你很擅长从专利内容中找出数学相关的内容并回答问题。
    你是如此优秀，因为你能把难题分解成它们的组成部分，
    回答各个组成部分，然后把它们组合在一起，来回答更广泛的问题.

    这里有一个问题:
    {input}"""

    automotive_template = """你是一个非常优秀的汽车工程师。
    你非常善于从专利内容中找出汽车的核心技术解决方案，并回答相应的问题。
    你擅长思考、反思、辩论、讨论和评估解决方案。

    这里有一个问题:
    {input}"""

    computerscience_template = """ 你是一个成功的计算机科学家。
    你有创造力和合作的热情，有远见、自信、解决问题的能力强;
    理解理论和算法，良好的沟通能力技能。你很擅长回答编程问题。
    你是如此的优秀，因为你知道如何解决问题，以命令式步骤描述解决方案。
    你擅长选择一个解决方案，可以很好的平衡时间复杂度和空间复杂度。

    这里有一个问题:
    {input}"""

    prompt_infos = [
        {
            "name": "physics",
            "description": "很适合回答关于物理的问题",
            "prompt_template": physics_template
        },
        {
            "name": "math",
            "description": "很适合回答数学问题",
            "prompt_template": math_template
        },
        {
            "name": "automotive",
            "description": "很适合回答汽车技术相关的问题",
            "prompt_template": automotive_template
        },
        {
            "name": "computer science",
            "description": "很适合回答计算机科学问题",
            "prompt_template": computerscience_template
        }
    ]

    llm = ChatOpenAI(temperature=0.9, model_name='gpt-4')

    #目标chain
    destination_chains = {}
    for p_info in prompt_infos:
        name = p_info["name"]
        prompt_template = p_info["prompt_template"]
        prompt = ChatPromptTemplate.from_template(template=prompt_template)
        chain = LLMChain(llm=llm, prompt=prompt)
        destination_chains[name] = chain

    destinations = [f"{p['name']}: {p['description']}" for p in prompt_infos]
    destinations_str = "\n".join(destinations)
    print(destinations_str)

    #定义模型选择模板
    MULTI_PROMPT_ROUTER_TEMPLATE = """给定一个原始文本输入到语言模型选择最适合输入的模型提示。
    您将获得可用提示符的名称和一个描述提示符最适合做什么。
    你也可以修改原始输入，如果你认为修改它最终会从语言模型中得到更好的响应。

    << FORMATTING >>
    返回一个带有JSON对象的标记代码片段，格式如下::
    ```json
    {{{{
        "destination": string \ 要使用的提示符名称或“DEFAULT”
        "next_inputs": string \ 原始输入的潜在修改版本
    }}}}
    ```

    REMEMBER: "destination"必须是候选提示符之一
    如果输入不是，则可以为“DEFAULT”
    非常适合任何候选人的提示。
    记住:“next_inputs”可以只是原始输入
    如果您认为不需要任何修改。

    << CANDIDATE PROMPTS >>
    {destinations}

    << INPUT >>
    {{input}}

    << OUTPUT (注意要包含json)>>"""

    router_template = MULTI_PROMPT_ROUTER_TEMPLATE.format(
        destinations=destinations_str
    )
    router_prompt = PromptTemplate(
        template=router_template,
        input_variables=["input"],
        output_parser=RouterOutputParser(),
    )
    router_chain = LLMRouterChain.from_llm(llm, router_prompt)

    #以上chain无效时，需要一个默认chain
    default_prompt = ChatPromptTemplate.from_template("{input}")
    default_chain = LLMChain(llm=llm, prompt=default_prompt)


    chain = MultiPromptChain(router_chain=router_chain,
                             destination_chains=destination_chains,
                             default_chain=default_chain, verbose=True
                             )
    response = chain.run("根据以下这些专利信息，回答问题：\"总结信息中描述的的核心技术要点\"。\n"
              "专利信息：本发明公开了一种基于物理学的改善粒子图像测速稳健性光流方法，包括如下步骤：S1、稳健能量泛函的构建；S2、复核数据项的构建；S3、平滑项的选择；S4、惩罚函数的构建；S5、模型能量泛函极小化处理；S6、光流计算；本发明提供一种基于物理学的改善粒子图像测速稳健性光流方法，本发明涵盖了稳健能量泛函的构建；复核数据项的构建；平滑项的选择；惩罚函数的构建；模型能量泛函极小化处理；光流计算活动粒子图像测速稳健性高；本发明中进一步在所述稳健能量泛函的构建过程中，首先构建基于物理学的光流约束方程；而后针对光流约束方程偏微分变化；最后依据变化结果生成稳健能量泛函，能量泛函通用性高。本发明公开了一种居民区电动汽车充电负载预测与配置方法，用于预测住宅区内电动汽车充电桩的电能消耗量及充电桩的配置方案，包括如下步骤：通过建立数学模型分析电动汽车动力电池的充电特性，对居民区原始负荷序列进行平稳化处理，计算平稳序列自相关与偏自相关函数，采用ARIMA数学模型对电动汽车充电桩的充电量进行定结合参数估计，对居民区新接入电动汽车的总负荷功率进行预测，对居民区变压器总容量进行优化调整配置。该方法统分析居民区电动汽车的充电特性，包括动力电池充电特征、出行时间概率分布、起始充电时间以及充电时长、日行驶里程等数学模型。")

    print(response)

if __name__ == "__main__":

    # simpleChain()
    # simpleSequentialChain()
    # sequentialChain()
    routerChain()
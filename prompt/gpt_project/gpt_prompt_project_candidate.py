from prettytable import PrettyTable

from prompt import gpt_cases, init_gpt
from prompt.gpt_project import gpt_project_cases


def generate_candidate_prompts(description, test_cases, number_of_prompts):
  outputs = init_gpt.client.chat.completions.create(
      model='gpt-4',
      messages=[
          {"role": "system", "content": """您的工作是为GPT-4生成系统提示，给出用例和一些测试用例的描述。

您将生成的提示将用于技术主题的研究，而用于技术分析的json输出是唯一可能的输出。

在生成的提示符中，你应该用通俗易懂的语言描述AI的行为。包括它将看到的内容，以及允许输出的内容。创造性地使用提示以获得最好的结果。AI知道它是一个AI——你不需要告诉它。

你将根据你的提示的表现来评分。但是不要作弊!您不能在提示中包含关于测试用例的细节。任何带有示例的提示将被取消。

最重要的是，只输出提示符。不要在你的信息中包含任何其他内容。"""},
          {"role": "user", "content": f"下面是一些测试用例::`{test_cases}`\n\n下面是用例的描述: `{description.strip()}`\n\n输出你的prompt, 不要给出其它额外信息. 有创造性一点."}
          ],
      temperature=.9,
      n=number_of_prompts)

  prompts = []

  for i in outputs.choices:
    prompts.append(i.message.content)
  return prompts

def t_candidate_prompts(test_cases, prompts):
  prompt_results = {prompt: {'correct': 0, 'total': 0} for prompt in prompts}

  # Initialize the table
  table = PrettyTable()
  table.field_names = ["Prompt", "Expected"] + [f"Prompt {i+1}-{j+1}" for j, prompt in enumerate(prompts) for i in range(prompts.count(prompt))]


  # Wrap the text in the "Prompt" column
  table.max_width["Prompt"] = 100


  for test_case in test_cases:
      row = [test_case['prompt'], test_case['answer']]
      for prompt in prompts:
          print(f'当前生成的prompt : {prompt}')
          print(f"当前参数 : {test_case['prompt']}")
          solution = init_gpt.client.chat.completions.create(
              model='gpt-4',
              messages=[
                  {"role": "system", "content": prompt},
                  {"role": "user", "content": f"{test_case['prompt']}"}
              ],
              max_tokens=1000,
              temperature=0,
          ).choices[0].message.content

          print(f'方案 ： {solution} ')
          isSame = compareDemo(solution, test_case['answer'])
          status = "✅" if isSame else "❌"
          row.append(status)

          # Update model results
          if isSame:
              prompt_results[prompt]['correct'] += 1
          prompt_results[prompt]['total'] += 1

      table.add_row(row)

  print(table)

  # Calculate and print the percentage of correct answers and average time for each model
  best_prompt = None
  best_percentage = 0
  for i, prompt in enumerate(prompts):
      correct = prompt_results[prompt]['correct']
      total = prompt_results[prompt]['total']
      percentage = (correct / total) * 100
      print(f"Prompt {i+1} got {percentage:.2f}% correct.")
      if percentage > best_percentage:
          best_percentage = percentage
          best_prompt = prompt

  print(f"The best prompt was '{best_prompt}' with a correctness of {best_percentage:.2f}%.")


def compareDemo(x, testCase) -> bool:
    content = init_gpt.client.chat.completions.create(
        model='gpt-4',
        messages=[
            {"role": "system", "content": """您的工作是某个研发技术主题分析，判断不同技术分析之间的相似性。

您的输出将用于分类器，'true'和'false'是唯一可能的输出。

在对两个技术分析语言描述进行对比时，需要对比两个方面:1.两种分析的数据格式是否相同，比如是否都是固定字段的json格式。2.两种分析的技术主题和细节描述是否相似，可以运用triz理论得到类似的分析结论。

你将根据两种分析的内容打一个相似分数，比对技术细节点，匹配一致的技术细节点越多，分数越高，结构不一致的情况下为0分，满分设置为100分。
分数若超过85，则判断为两者相似，否则的话为不相似。

最重要的是，只输出'true'或者'false'。不要在你的信息中包含任何其他内容"""},
            {"role": "user", "content": f"对比以下两个技术描述：描述1：{x} \n 描述2：{testCase}"}
        ],
        max_tokens=2,
        temperature=.1,
    ).choices[0].message.content
    return content == 'true'

if __name__ == "__main__":

    # candidate_prompts = generate_candidate_prompts(gpt_project_cases.description, gpt_project_cases.test_cases, gpt_project_cases.number_of_prompts)
    candidate_prompts = gpt_project_cases.candidate_project_prompts
    t_candidate_prompts(gpt_project_cases.test_cases, candidate_prompts)
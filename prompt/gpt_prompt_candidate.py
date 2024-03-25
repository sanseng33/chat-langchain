from prettytable import PrettyTable

import init_gpt
from prompt import gpt_cases


def generate_candidate_prompts(description, test_cases, number_of_prompts):
  outputs = init_gpt.client.chat.completions.create(
      model='gpt-4',
      messages=[
          {"role": "system", "content": """Your job is to generate system prompts for GPT-4, given a description of the use-case and some test cases.

The prompts you will be generating will be for classifiers, with 'true' and 'false' being the only possible outputs.

In your generated prompt, you should describe how the AI should behave in plain English. Include what it will see, and what it's allowed to output. Be creative in with prompts to get the best possible results. The AI knows it's an AI -- you don't need to tell it this.

You will be graded based on the performance of your prompt... but don't cheat! You cannot include specifics about the test cases in your prompt. Any prompts with examples will be disqualified.

Most importantly, output NOTHING but the prompt. Do not include anything else in your message."""},
          {"role": "user", "content": f"Here are some test cases:`{test_cases}`\n\nHere is the description of the use-case: `{description.strip()}`\n\nRespond with your prompt, and nothing else. Be creative."}
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
          x = init_gpt.client.chat.completions.create(
              model='gpt-3.5-turbo',
              messages=[
                  {"role": "system", "content": prompt},
                  {"role": "user", "content": f"{test_case['prompt']}"}
              ],
              logit_bias={
                  '1904': 100,  # 'true' token
                  '3934': 100,  # 'false' token
              },
              max_tokens=1,
              temperature=0,
          ).choices[0].message.content


          status = "✅" if x == test_case['answer'] else "❌"
          row.append(status)

          # Update model results
          if x == test_case['answer']:
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


if __name__ == "__main__":

    candidate_prompts = generate_candidate_prompts(gpt_cases.description, gpt_cases.test_cases, gpt_cases.number_of_prompts)
    t_candidate_prompts(gpt_cases.test_cases, candidate_prompts)
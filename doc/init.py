import csv
import re
import json


def extract_info_from_logs(csv_file_path):
    results = []

    # 读取CSV文件
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            text = row[0]  # 假设每行只有一列，且该列为我们要分析的文本
            fixRequest(text, results)

    return results

def fixRequest(text, results):

    # 使用正则表达式提取CORRID和message的JSON内容
    # 更新正则表达式以提取CORRID和JSON内容
    corrid_search = re.search(r'CORRID:([^ ]+)', text)
    # 匹配message后面的完整JSON对象
    message_search = re.search(r'parameters:({.*?})(?=\s|$)', text)

    if corrid_search and message_search:
        try:
            message_json = json.loads(message_search.group(1))
            prompt = message_json.get('user_prompt', '')
            # effect = message_json.get('prompt_placeholder_map', {}).get('effect', '')
            # topic = message_json.get('prompt_placeholder_map', {}).get('topic', '')
            # patent = message_json.get('prompt_placeholder_map', {}).get('patent_source', '')
            # paper = message_json.get('prompt_placeholder_map', {}).get('paper_source', '')
            # title = message_json.get('prompt_placeholder_map', {}).get('title', '')
            # metadata = message_json.get('prompt_placeholder_map', {}).get('metadata', '')
            # domain_desc = message_json.get('prompt_placeholder_map', {}).get('domain_desc', '')
            # domain = message_json.get('prompt_placeholder_map', {}).get('domain', '')
            # pum = message_json.get('prompt_placeholder_map', {}).get('pum', '')
            # pum_desc = message_json.get('prompt_placeholder_map', {}).get('pum_desc', '')

            # 构造并返回结果字典
            # result_dict = {
            #     'CORRID': corrid_search.group(1),
            #     'lang': lang,
            #     'effect': effect,
            #     'topic': topic,
            #     'patent_source': patent,
            #     'paper_source': paper,
            #     'title': title,
            #     'domain_desc': domain_desc,
            #     'domain': domain,
            #     'pum': pum,
            #     'pum_desc': pum_desc,
            #     'metadata': metadata
            #
            # }
            # prompt = '从现在开始你是一个技术专家，同时也是一个专利研发人员，你擅长写各类立项报告，擅长围绕技术主题与技术效果等信息，结合你的自身知识储备，撰写技术立项的相关分析内容。假设现在有一个技术主题“锂电池”，和一个技术效果“提高能量密度”，并且存在一个专利申请量各年份的趋势数据为：2014:1781,2015:6274,2016:14675,2017:8855,2018:593,2019:251,2020:98,2021:95,2022:25,2023: 0 \n和一个文献各年份数量的数据为：2014:1320,2015:6274,2016,:14675,2017:8800,2018:1304,2019:120,2020:88,2021:90,2022:25,2023: 0 \n依据以上数据，结合自身经验，可以得出以下技术背景的结论：{{\"background\":\"随着全球对能源的需求不断上升以及对环境可持续性的重视日增，锂电池因其高效性和清洁能源属性，在电动汽车和可再生能源存储等关键领域扮演着举足轻重的角色。能量密度，作为衡量锂电池性能的核心指标之一，它直接决定了电池的续航能力、存储效能以及其在不同应用领域的适用性。\n\n近几年来，全球研究界在提升锂电池能量密度方面取得了显著的突破。专利申请在某一年达到了高峰，随后呈逐年下降趋势，这反映出在提升锂电池能量密度的领域曾经发生了一次科技创新热潮。而从相关文献申请的数据来看，虽然专利申请数量呈下降趋势，但在提升锂电池能量密度方面的研究活动并未减弱，尤其是在中间的几年，相关文献的申请量甚至呈上升趋势，表明学术界对这一领域的关注度仍然高涨。\n\n尽管近年来专利申请数量趋于稳定，但从更长远的角度来看，提高锂电池能量密度的研究仍将是未来发展的主流方向，特别是考虑到对环保的需求和可再生能源需求的持续增长。电动汽车和可持续能源系统尤其需要性能更优的锂电池来满足其运行需求。此外，当前的研究和文献也表明，关于提升锂电池能量密度的理论研究依然在深入进行之中。\n\n总的来说，提升锂电池的能量密度是一个长期而又需要持续投入的任务。随着科技的进步和市场需求的不断拉动，这一领域将迎来更多的研发任务和发展机遇。\"}}\n\n现在对于一个新的技术主题\"{topic}\"，和一个技术效果\"{effect}\"，以及一个专利申请量的数据为：{patent_source}，和文献数据：{paper_source}。请根据提供的数据，仔细分析“{topic}”的“{effect}”技术领域的发展趋势。请确保你的观察与数据走势一致，并在给出技术背景分析时，明确基于这些观察。请注意，你的分析应该完全依赖于数据走势，并确保结论与观察到的趋势相符。\n\n要求: 1,输出应该是一个json，json中只包含background的信息。除了json外不要输出其它额外信息。2,请确保生成的内容严谨。请一步一步的思考，对专利或文献趋势的总结不要包含具体的年份。3，不要使用第一人称描述，而是第三人称。'
            # prompt = '从现在开始你是一个技术专家，同时也是一个专利研发人员，你擅长写各类立项报告，擅长围绕技术主题与技术效果等信息，结合你的自身知识储备，撰写技术立项的相关分析内容。假设现在有一个技术主题“磷酸铁锂电池”，和一个技术效果“提高能量密度”。\n结合自身经验，得出以下技术现状分析的结论：\n{{\n  \"current_situation\": \"目前，锂电池技术发展迅猛，已成为众多领域最重要的能量存储解决方案之一。磷酸铁锂（LiFePO4）电池以其优异的安全性能和较长的循环寿命在市场中占有一席之地，特别是在电动汽车和大型储能领域。\n然而，与其他类型的锂电池（如锂钴酸锂电池、锂锰酸锂电池）相比，磷酸铁锂电池的能量密度相对较低，这限制了其在高能量密度需求领域的应用，如便携式电子产品和某些特定类型的电动汽车。\n在电动汽车领域，磷酸铁锂电池的使用有助于降低整车成本并提供良好的安全性能，但其较低的能量密度意味着车辆的续航能力有限。随着消费者对电动汽车续航里程的需求日益增加，提高磷酸铁锂电池的能量密度成为业界关注的焦点。\n在大型储能领域，磷酸铁锂电池被广泛应用于储存来自可再生能源的电能，其长寿命和稳定性使其成为理想的选择。然而，为了提升储能系统的整体经济性和减小所需的空间，提高能量密度仍然是一个关键问题。\n在便携式电子产品领域，由于磷酸铁锂电池的能量密度相对较低，其应用相对有限，市场主要被其他高能量密度的锂电池所占据。研发更高能量密度的磷酸铁锂电池对于拓展其在这一领域的市场份额具有重要意义。\n\",\n  \"technical_characteristics_and_challenges\": \"作为项目公司主要关注的类型，磷酸铁锂电池具有较高的安全性和循环寿命，适用于电动汽车、储能等领域。然而，其能量密度相对较低，主要受到以下因素的影响：\n1. 正负极材料能量密度限制：磷酸铁锂正极材料的电化学活性相对较低，导致其能量密度有限。通过开发新型高能量密度材料或改进现有材料的结构和性能，有望提升磷酸铁锂电池的能量密度。\n2. 电解质与界面问题：电解质的离子传导性和电极材料界面的稳定性对电池的能量密度和循环寿命有着直接影响。开发新型电解质或优化电极/电解质界面的处理技术，是提高磷酸铁锂电池性能的重要研究方向。\n3. 循环寿命与稳定性：磷酸铁锂电池虽然在循环寿命方面表现优异，但在追求更高能量密度的过程中，保持其长寿命和高稳定性仍是一个挑战。\n4. 应用领域的特定需求：\n- 在电动汽车领域，除了提高能量密度提升续航里程外，优化磷酸铁锂电池的快充性能也是重要研究方向。\n- 在大型储能领域，磷酸铁锂电池需要不仅要有高能量密度，还需要有良好的低温性能和长寿命。\n- 在便携式电子产品领域，提高能量密度的同时，磷酸铁锂电池还需要满足更高的安全性和更低的成本要求。\n\",\n  \"technological_path\": \"为应对上述技术挑战，推动磷酸铁锂电池能量密度的提升，建议采取以下技术路径：\n1.高活性正极材料的研发：通过纳米技术和材料掺杂提高磷酸铁锂正极材料的电化学活性和电导性。\n2.先进电解质和界面工程：开发高离子导电性电解质，并改善电极材料与电解质的界面稳定性。\n3.系统集成和模块优化：通过电池管理系统的优化和电池模块设计的创新，提高整个电池系统的能量密度和运行效率。\n4.热管理系统的优化：研发高效的热管理系统，确保电池在高能量密度运行条件下的稳定性和安全性。\n\"\n}}\n\n 现在有一个新的技术主题“{topic}”，和一个技术效果“{effect}”，结合你自身经验，给出类似的现状分析。\n 要求：\n 1，输出必须为一个json,与样例类似，需要包含\'current_situation\',\'technical_characteristics_and_challenges\',\'technological_path\'这三个字段,每个字段的值都应该是字符串格式。除json外不要输出其它额外信息。另外current_situation字段中需要包含详细的应用领域方面的信息，并确保其和{topic}的{effect}的相关性。\n 2，请一步一步的思考，确保生成的内容严谨。\n 3，注意详细描述有关应用领域的部分。\n 4, 请注意，本节的目标是明确和详细地描述技术现状分析，不需要在最后添加总结性或者归纳性质的段落。'
            # prompt = '你是一名在“{topic}”领域拥有丰富经验的研发专员，特别擅长撰写研究报告。现在请你基于{topic}的相关研发知识，结合在商业、技术和成本等方面的方法论思路，为我们撰写一个关于“{title}”的技术预研报告中的“研究内容”部分。这份报告主要针对公司的研发决策层，目的是清晰地展示在这个技术项目中我们将具体研究哪些内容，并规划出大致的研究方案。\n\n在内容编排时，请紧密结合以下信息：本报告围绕“{topic}”这一技术关键词展开，旨在达到“{effect}”的技术效果。{domain_desc}{domain}，{pum_desc}{pum}。请在撰写时，充分考虑到这些要素，并确保内容的准确性和详实性。\n\n报告的内容格式和要求如下：\n\n研究内容及目标：\n请生成至少3个约300字的子段落，详细描述具体的研究目标和计划。\n1 [研究目标]：阐述项目的最终目标和期望达到的成果。\n2 [研究方向及重点]：明确研究的主要方向，并细分出各个研究重点。\n\n2.1 [子项名称]：描述具体的研究内容和预期的成果。\n2.2 [子项名称]：描述具体的研究内容和预期的成果。\n2.3 [子项名称]：描述具体的研究内容和预期的成果。\n···（根据需要添加更多子项）\n3 [研究计划和方法]：概述整个研究项目的计划安排和采用的研究方法。\n请保持写作风格的正式性和学术性，确保内容的准确无误。'
            id = corrid_search.group(1)
            if id is None or prompt is None:
                return
            new_dict = {
                'CORRID': id,
                'prompt_con': prompt

            }
            results.append(new_dict)
        except json.JSONDecodeError:
            pattern = r'user_prompt":"(.*?)","model'  # 使用非贪婪匹配，提取每对 PT 和 ER 之间的内容

            prompt = re.findall(pattern, text, re.DOTALL)
            id = corrid_search.group(1)
            if id is None or prompt is None or prompt is []:
                return
            new_dict = {
                'CORRID': id,
                'prompt_con': prompt[0]

            }
            results.append(new_dict)
            # 如果JSON解析失败，返回None
    return results
def fixResp(text, results, lastline):
    # 使用正则表达式提取CORRID和message的JSON内容
    corrid_search = re.search(r'CORRID:([^ ]+)', lastline)

    # 匹配message后面的完整JSON对象
    # message_search = re.search(r'resp:({.*?})(?=\s|$)', text)
    # message_search = re.search(r'resp:\s*(\{.*\})', text, re.DOTALL)
    message_search = lastline.split('resp:')[-1]
    # if not (message_search.startswith("{")):
    #     message_search = "{"+message_search
    if corrid_search:
        try:

            # 构造并返回结果字典
            result_dict = {
                'CORRID': corrid_search.group(1),
                'resp': message_search,
            }
            results.append(result_dict)
        except json.JSONDecodeError:
            # 如果JSON解析失败，返回None
            return
    return results
def format_corrids(corrid_dicts):
    # 从每个字典中提取CORRID值
    corrids = [d['CORRID'] for d in corrid_dicts]
    # 将CORRID值转换成一个字符串，并用逗号和双引号分隔
    corrids_str = ','.join(f'"{cid}"' for cid in corrids)
    # 格式化最终字符串
    final_str = f'CORRID in ({corrids_str})'
    return final_str


def extract_info_from_resp(csv_file_path):
    results = []

    # 读取CSV文件
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            text = row[0]  # 假设每行只有一列，且该列为我们要分析的文本
            fixResp(text, results)

    return results

import os
def extract_relevant_logs(folder_path):
    """
    This function walks through all txt files in the specified folder,
    reads each line of each file, and prints lines that contain any of
    the specified keywords.
    """
    # Keywords to check in each log line
    # keywords = ["BackgroundModelWork 调用gpt请求", "[callGPT] gpt调用结果"]
    # keywords = ["SituationModelWork 调用gpt请求", "[callGPT] gpt调用结果"]
    # keywords = ["TargetModelWork 调用gpt请求", "[callGPT] gpt调用结果"]
    # keywords = ["current_situation 调用gpt请求", "[callGPT] gpt调用结果"]
    # keywords = ["SituationModelWork 调用gpt请求", "[callGPT] gpt调用结果"]
    # keywords = ["SituationModelWork 调用gpt请求", "[callGPT] gpt调用结果"]



    # keywords = ["[callGPT] gpt调用结果", "研究内容及目标"]
    keywords = ["[callGPT] gpt调用结果", "innovation_point"]
    # keywords = ["[SituationModelWork] ai response"]
    keywordsResp = ["[callGPT] 参数前置处理","project_submission"]
    results = []
    resultsResp = []
    # Walking through the folder
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)
                currentline = ""
                # Reading each file line by line
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line in f:

                        if ('2024-03-' in line):
                            lastline = currentline
                            currentline = line
                            if (lastline != '' and all(keyword in lastline for keyword in keywordsResp)):
                                print(line)
                                results = fixRequest(lastline, results)
                            if (lastline != '' and all(keyword in lastline for keyword in keywords)):
                                resultsResp = fixResp(line, resultsResp, lastline)
                        else:
                            currentline = currentline + line
                        # Check if any of the keywords is in the line


    return results, resultsResp

if __name__ == "__main__":
    # results = extract_info_from_logs("D://data//eureka-project-tar-req.csv")
    # resultResp = extract_info_from_resp("D://data//eureka-project-tar-rep2.csv")
    # resultResp2 = extract_info_from_resp("D://data//eureka-project-tar-rep.csv")
    # body = resultResp + resultResp2

    results, body = extract_relevant_logs("D://data//log//")

    corrid_to_prompt_con = {item['CORRID']: item['prompt_con'] for item in results}
    # print(corrid_to_prompt_con)
    # 合并两个列表
    merged_list = []
    for item in body:
        print(item['CORRID'])
        # 如果在第二个列表中找到相同的CORRID
        if item['CORRID'] in corrid_to_prompt_con:

            # 合并字典
            mergeditem = {
                'prompt_con': corrid_to_prompt_con[item['CORRID']],
                'resp': item['resp']
            }
            # print(mergeditem)
            merged_list.append(mergeditem)

    csv_file_name = 'D://data//keypatent.csv'
    with open(csv_file_name, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['prompt_con', 'resp'])
        writer.writeheader()
        for data in merged_list:
            writer.writerow(data)
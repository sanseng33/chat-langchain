import json
import re

import requests

# 设置您的访问参数
BASE_URL = 'http://git.patsnap.com/api/v4'
PROJECT_ID = '7193'  # 您的项目ID
COMMIT_SHA = 'dfe5e3ed763b53644290c040ed53ba85c31f4e09'  # 您的提交ID（SHA值）
ACCESS_TOKEN = 'M8oe7aMuVGvyKPX1uaNH'  # 您的个人访问令牌


def commit_short_id(project_id: str, commit_sha: str) -> str:
    # 构建API URL
    # url = f"{BASE_URL}/projects/{PROJECT_ID}/repository/commits/{COMMIT_SHA}/diff?unidiff=true"
    url = f"{BASE_URL}/projects/{project_id}/repository/commits/{commit_sha}"

    # 发送GET请求获取提交详情
    headers = {'PRIVATE-TOKEN': f'{ACCESS_TOKEN}'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        commit_info = response.json()
        print("提交详情：")
        print(commit_info)
        return commit_info['short_id']
    else:
        print("获取提交详情失败，状态码：", response.status_code)
        return "0"


def commit_diff(project_id: str, commit_sha: str) -> str:
    # 构建API URL
    url = f"{BASE_URL}/projects/{project_id}/repository/commits/{commit_sha}/diff?unidiff=true"
    # 发送GET请求获取提交详情
    headers = {'PRIVATE-TOKEN': f'{ACCESS_TOKEN}'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        commit_info = response.json()
        result = {}
        # 遍历列表
        for item in commit_info:
            new_path = item['new_path']
            diff = item['diff']
            # 使用正则表达式匹配 \n+ 后的内容
            matches = re.findall(r'\n\+([^\n]+)', diff)
            # 过滤掉以import开头且以;结束的字符串
            filtered_matches = [match for match in matches if
                                not (match.strip().startswith('import') and match.strip().endswith(';'))]

            # 将所有匹配到的内容组装成一个新的字符串
            new_string = ' \n '.join(filtered_matches)
            if new_path in result:
                result[new_path].append(new_string)
            else:
                result[new_path] = [new_string]

        output_json = json.dumps(result)
        print("提交差异内容:\n", output_json)
        return output_json
    else:
        print("获取提交差异内容失败，状态码：", response.status_code)
        return "0"


def commit_all(project_id: str) -> str:
    # 构建API URL
    # url = f"{BASE_URL}/projects/{PROJECT_ID}/repository/commits/{COMMIT_SHA}/diff?unidiff=true"
    url = f"{BASE_URL}/projects/{project_id}/repository/commits?ref_name=master&since=2024-03-01T00:00:00&first_parent=false"

    # 发送GET请求获取提交详情
    headers = {'PRIVATE-TOKEN': f'{ACCESS_TOKEN}'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        commit_info = response.json()
        print("提交列表：")
        print(commit_info)
        resp = []
        for item in commit_info:
            result = {'short_id': item['short_id'], 'title': item['title']}
            resp.append(result)
        return json.dumps(resp)
    else:
        print("获取提交列表失败，状态码：", response.status_code)
        return "0"


if __name__ == "__main__":
    commit_diff(PROJECT_ID, COMMIT_SHA)

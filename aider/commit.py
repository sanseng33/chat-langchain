import json
import re
from typing import Dict

import requests

# 设置您的访问参数
BASE_URL = 'http://git.patsnap.com/api/v4'
PROJECT_ID = '7193'  # 您的项目ID
COMMIT_SHA = 'dfe5e3ed763b53644290c040ed53ba85c31f4e09'  # 您的提交ID（SHA值）
ACCESS_TOKEN = 'M8oe7aMuVGvyKPX1uaNH'  # 您的个人访问令牌
HEADERS = {'PRIVATE-TOKEN': ACCESS_TOKEN}

def construct_url(project_id: str, type: str, commit_sha: str = '') -> str:
    if type == "diff":
        return f"{BASE_URL}/projects/{project_id}/repository/commits/{commit_sha}/diff?unidiff=true"
    elif type == "commit":
        return f"{BASE_URL}/projects/{project_id}/repository/commits/{commit_sha}"
    else:
        return f"{BASE_URL}/projects/{project_id}/repository/commits?ref_name=master&since=2024-03-01T00:00:00&first_parent=false"


def get_response(url: str) -> Dict:
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"请求失败，状态码：{response.status_code}")
        return {}


def format_commit_diff(commit_info: Dict) -> str:
    result = {}
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
    return json.dumps(result)



def commit_short_id(project_id: str, commit_sha: str) -> str:
    url = construct_url(project_id, "commit", commit_sha=commit_sha)
    commit_info = get_response(url)
    return commit_info['short_id'] if commit_info else "0"

def commit_diff(project_id: str, commit_sha: str) -> str:
    url = construct_url(project_id, "diff", commit_sha=commit_sha)
    commit_info = get_response(url)
    output_json = format_commit_diff(commit_info) if commit_info else "0"
    print("提交差异内容:<br />", output_json)
    return output_json

def commit_all(project_id: str) -> str:
    url = construct_url(project_id, "commit_all")
    commit_info = get_response(url)
    resp = [{'short_id': item['short_id'], 'title': item['title']} for item in commit_info]
    print("提交列表：", resp)
    return json.dumps(resp)


if __name__ == "__main__":
    commit_diff(PROJECT_ID, COMMIT_SHA)

import json
import os

from langchain_community.chat_models import ChatOpenAI

from aider.commit import commit_short_id, commit_diff
from aider.file_content import file_content
from aider.template import parseCode

PROJECT_ID = '7193'  # 您的项目ID
COMMIT_SHA = 'dfe5e3ed763b53644290c040ed53ba85c31f4e09'  # 您的提交ID（SHA值）


def codeParse(commit_sha: str) -> str:
    shortId = commit_short_id(PROJECT_ID, commit_sha)
    commitInfo = commit_diff(PROJECT_ID, commit_sha)
    commitJson = json.loads(commitInfo)
    resp = []
    for key, value in commitJson.items():
        content = file_content(PROJECT_ID, shortId, key)
        result = parseCode(key, content)
        print('当前提交文件：')
        print(key)
        print('review结果：')
        print(result)
        item = {'file': key, 'review': result}
        resp.append(item)
    return json.dumps(resp)

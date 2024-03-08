import urllib

import requests
import base64
from urllib.parse import quote_plus

# 设置您的访问参数
BASE_URL = 'http://git.patsnap.com/api/v4'
PROJECT_ID = '7193'  # 您的项目ID
COMMIT_SHA = 'dfe5e3ed'  # 您的提交ID（SHA值）
ACCESS_TOKEN = 'M8oe7aMuVGvyKPX1uaNH'  # 您的个人访问令牌
FILE_PATH = 'eureka-core%2Fsrc%2Fmain%2Fjava%2Fcom%2Fpatsnap%2Feureka%2Fmanager%2Fpermission%2FPackageManager.java'  # 文件完整路径


def file_content(project_id: str, commit_id: str, file_path: str) -> str:
    if isinstance(file_path, str):
        file_path = quote_plus(file_path)
    # 构建API URL
    url = f"{BASE_URL}/projects/{project_id}/repository/files/{file_path}?ref={commit_id}"

    # 发送GET请求获取提交详情
    headers = {'PRIVATE-TOKEN': f'{ACCESS_TOKEN}'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        commit_info = response.json()
        print("文件详情：")
        print(commit_info)
        return base64.b64decode(commit_info['content']).decode()
    else:
        print("获取文件详情失败，状态码：", response.status_code)


def file_content_with_master(project_id: str, file_path: str) -> str:
    if isinstance(file_path, str):
        file_path = quote_plus(file_path)
    # 构建API URL
    url = f"{BASE_URL}/projects/{project_id}/repository/files/{file_path}?ref=master"

    # 发送GET请求获取提交详情
    headers = {'PRIVATE-TOKEN': f'{ACCESS_TOKEN}'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        commit_info = response.json()
        print("文件详情：")
        print(commit_info)
        return base64.b64decode(commit_info['content']).decode()
    else:
        print("获取文件详情失败，状态码：", response.status_code)
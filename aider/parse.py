import json
import os

from langchain_community.chat_models import ChatOpenAI

from aider.commit import commit_short_id, commit_diff
from aider.file_content import file_content
from aider.template import parseCode

PROJECT_ID = '7193'  # 您的项目ID
COMMIT_SHA = 'dfe5e3ed763b53644290c040ed53ba85c31f4e09'  # 您的提交ID（SHA值）


def calculate_splits(string):
    # 计算字符串中的行数
    lines = string.split('\n')
    num_lines = len(lines)

    # 判断行数，并进行相应的分割
    if num_lines > 200:
        return 3
    elif num_lines > 100:
        return 2
    else:
        return 1


def split_string(string, num_splits):
    # Split the string into lines
    lines = string.split('\n')
    num_lines = len(lines)

    # Calculate the size of each split
    split_size = num_lines // max(num_splits, 1)  # Avoid division by zero
    splits = [lines[i * split_size:(i + 1) * split_size] for i in range(num_splits)]
    if num_splits == 1:
        splits = [lines]  # Return the original string if only one split

    return splits


def addSplitLine(result: str, index: int):

    resp = []
    for item in result:
        # 分割lineNumber，处理可能存在的多个范围
        ranges = item['lineNumber'].split(', ')
        new_ranges = []
        for range_str in ranges:
            # 拆分每个范围字符串
            start, end = range_str.split('-')

            # 将index加到拆分后的数字上，并转换为字符串
            start_index = str(int(start) + index)
            end_index = str(int(end) + index)

            # 重新组合每个范围，并添加到新范围列表中
            new_range = f'{start_index}-{end_index}'
            new_ranges.append(new_range)

        # 使用逗号连接处理后的所有范围，形成新的lineNumber字符串
        new_lineNumber = ', '.join(new_ranges)

        # 构建新的字典对象添加到响应列表中
        line = {'lineNumber': new_lineNumber, 'reviewComment': item['reviewComment']}
        resp.append(line)
    return resp

def codeParse(commit_sha, continuation_data=None):
    # Initialize variables for first call or continuation
    if continuation_data is None or continuation_data is {}:
        # Initial call setup
        short_id = commit_short_id(PROJECT_ID, commit_sha)
        commit_info = commit_diff(PROJECT_ID, commit_sha)
        commit_json = json.loads(commit_info)
        key_list = list(commit_json.keys())  # Convert keys to a list for ordered processing
        current_key_index = 0  # Start processing from the first key
        current_split_index = 0  # Start from the first split
    else:
        # Continuation call setup
        commit_json = continuation_data['commit_json']
        short_id = continuation_data['short_id']
        key_list = continuation_data['key_list']
        current_key_index = continuation_data['current_key_index']
        current_split_index = continuation_data['current_split_index']
        print('continuation_data \n', continuation_data)

    while current_key_index < len(key_list):
        key = key_list[current_key_index]
        print('key_list \n', continuation_data)
        content = file_content(PROJECT_ID, short_id, key)
        num_splits = calculate_splits(content)
        splits = split_string(content, num_splits)
        print('splits \n', len(splits))
        if current_split_index < len(splits):
            split_content = '\n'.join(splits[current_split_index])
            result = parseCode(key, split_content)
            result = addSplitLine(result, current_split_index)
            print('current_split_index \n', current_split_index)
            item = {'file': key, 'review': result}
            # Check if this is the last split of the last key
            is_last_key = current_key_index == len(key_list) - 1
            is_last_split = current_split_index == len(splits) - 1

            print('is_last_key \n', is_last_key)
            print('is_last_split \n', is_last_split)

            if is_last_key and is_last_split:
                # If processing the last split of the last key, set continuation_data to None
                continuation_data = None
            else:
                # Prepare for next split or next key
                current_split_index += 1
                print('add index \n', current_split_index)
                if current_split_index >= len(splits):
                    # Move to the next key and reset split index
                    current_key_index += 1
                    current_split_index = 0

                # Prepare continuation data
                continuation_data = {
                    'commit_json': commit_json,
                    'short_id': short_id,
                    'key_list': key_list,
                    'current_key_index': current_key_index,
                    'current_split_index': current_split_index,
                }

            return json.dumps({'data': item, 'continuation_data': continuation_data})

        # If there's no more data to process, return a final response indicating completion
    return json.dumps({'data': None, 'continuation_data': None})

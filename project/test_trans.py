import trans
import os
import pandas as pd
import csv
import chardet

def detect_file_encoding(file_path):
    with open(file_path, 'rb') as file:
        raw_data = file.read()
    result = chardet.detect(raw_data)
    return result


app_key = '68710a11f941b9ca'
app_secret = 'sCMqHtZ9htOo26oiAsSgPBZ46srV9pJR'
src_lang = 'zh-CHS'
dest_lang = 'en'

def check_create(p):
    if not os.path.exists(p):
        with open(p, 'w', encoding='utf-8') as f:
            pass

def process_csv_with_pandas(input_file_path, output_file_path):
    # 使用pandas读取csv文件
    df = pd.read_csv(input_file_path, header=None, encoding='GB2312')  # 假设CSV没有标题行

    # 检查至少有两列
    if df.shape[1] < 2:
        raise ValueError("CSV文件至少需要包含两列数据")

    # 应用翻译函数到每列的每个元素
    df[0] = df[0].apply(trans.translate)  # 第一列翻译
    df[1] = df[1].apply(trans.translate)  # 第二列翻译

    # 保存到新的CSV文件，如果文件不存在会自动创建
    df.to_csv(output_file_path, index=False, header=False, mode='a', encoding='utf-8')

# 使用此函数处理文件
input_file_path = 'D://data//关键专利.csv'
output_file_path = 'D://data//关键专利英文.csv'
process_csv_with_pandas(input_file_path, output_file_path)
#
# encoding_info = detect_file_encoding(input_file_path)
# print(encoding_info)


import pandas as pd
import os

# 路径设置
xlsx_path = 'd://project_prompt.xlsx'

# 读取xlsx文件
df = pd.read_excel(xlsx_path)

# 检查output_file.csv文件是否存在，如果不存在则创建
def check_create(p):
    if not os.path.exists(p):
        with open(csv_path, 'w', encoding='utf-8') as f:
            pass

# 轮询每一行
for index, row in df.iterrows():
    # 取第一列的内容
    first_column_content = str(row[0])
    # 检查字符串中是否包含'dev'
    if '并且存在一个专利申请量各年份的趋势数据为' in first_column_content:
        csv_path = 'd://data//技术背景.csv'
        check_create(csv_path)
        # 将满足条件的行写入csv文件
        row.to_frame().T.to_csv(csv_path, mode='a', header=not os.path.exists(csv_path), index=False, encoding='utf-8')
        continue
    if '得出以下技术现状分析的结论' in first_column_content:
        csv_path = 'd://data//技术现状分析.csv'
        check_create(csv_path)
        # 将满足条件的行写入csv文件
        row.to_frame().T.to_csv(csv_path, mode='a', header=not os.path.exists(csv_path), index=False, encoding='utf-8')
        continue
    if '技术预研报告中的“研究内容”部分' in first_column_content:
        csv_path = 'd://data//研究内容.csv'
        check_create(csv_path)
        # 将满足条件的行写入csv文件
        row.to_frame().T.to_csv(csv_path, mode='a', header=not os.path.exists(csv_path), index=False, encoding='utf-8')
        continue
    if '重点玩家分析' in first_column_content:
        csv_path = 'd://data//重点玩家分析.csv'
        check_create(csv_path)
        # 将满足条件的行写入csv文件
        row.to_frame().T.to_csv(csv_path, mode='a', header=not os.path.exists(csv_path), index=False, encoding='utf-8')
        continue
    if '参考IDC技术市场分类' in first_column_content:
        csv_path = 'd://data//技术路线.csv'
        check_create(csv_path)
        # 将满足条件的行写入csv文件
        row.to_frame().T.to_csv(csv_path, mode='a', header=not os.path.exists(csv_path), index=False, encoding='utf-8')
        continue
    if '结合行业技术体系和你自身的经验' in first_column_content:
        csv_path = 'd://data//技术路线图表.csv'
        check_create(csv_path)
        # 将满足条件的行写入csv文件
        row.to_frame().T.to_csv(csv_path, mode='a', header=not os.path.exists(csv_path), index=False, encoding='utf-8')
        continue
    if '对专利说明书的背景技术' in first_column_content:
        csv_path = 'd://data//关键专利.csv'
        check_create(csv_path)
        # 将满足条件的行写入csv文件
        row.to_frame().T.to_csv(csv_path, mode='a', header=not os.path.exists(csv_path), index=False, encoding='utf-8')



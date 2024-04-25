import requests
import hashlib
import uuid
import time
import json

def translate(text):
    app_key = '68710a11f941b9ca'
    app_secret = 'sCMqHtZ9htOo26oiAsSgPBZ46srV9pJR'

    src_lang = 'zh-CHS'
    dest_lang = 'en'

    youdao_url = "https://openapi.youdao.com/api"

    # 生成随机字符串
    salt = str(uuid.uuid4())
    # 获取当前时间戳
    curtime = str(int(time.time()))
    # 生成签名
    sign_str = app_key + text + salt + curtime + app_secret
    sign = hashlib.sha256(sign_str.encode('utf-8')).hexdigest()

    # 构建请求参数
    params = {
        'q': text,
        'from': src_lang,
        'to': dest_lang,
        'appKey': app_key,
        'salt': salt,
        'sign': sign,
        'signType': 'v3',
        'curtime': curtime
    }

    # 发送请求
    response = requests.post(youdao_url, data=params)
    # 解析响应内容
    result = response.json()

    # 输出翻译结果
    return result['translation'][0] if 'translation' in result else result

# 示例用法


translation = translate('')

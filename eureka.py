import requests
import json

def metadataDna(message):
    # Define the URL and the headers
    url = "http://localhost:8080/eureka/ai/chat/metadata"
    headers = {
        'Content-Type': 'application/json',
        'X-API-Version': '1.0',
        'X-PatSnap-Version': 'v1',
        'X-User-ID': '73b511eef4104afda2fef37bcd94c100',
        'x-patsnap-from': 'w-analytics-patent-view',
        'x-site-lang': 'en'
    }

    # Define the payload
    payload = {
        "message": message
    }

    # Make the POST request and get the response
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response_json = json.loads(response.text)
    if response_json['error_code'] is 0:
        return response_json['data']
    return []

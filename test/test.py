import requests
import json

session = requests.session()

url = "http://127.0.0.1:2023/connect"
with open('config.json', 'r') as fp:
    data = json.load(fp=fp)
json_data = json.dumps(data)  # 将数据编码为JSON格式

response = session.post(url, json=data)
print(response.cookies)


url = "http://127.0.0.1:2023/test"
response = session.get(url)
print(response.text)

url = "http://127.0.0.1:2023/close"
response = session.get(url)
print(response.text)

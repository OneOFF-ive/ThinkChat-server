import requests
import json

session = requests.session()

url = "http://127.0.0.1:2023/common/connect"
with open('config.json', 'r') as fp:
    data = json.load(fp=fp)
json_data = json.dumps(data)  # 将数据编码为JSON格式

response = session.post(url, json=data)
print(response.cookies)

url = "http://127.0.0.1:2023/common/select/records"
data = {"name": "test"}
response = session.post(url, json=data)
print(response.text)

url = "http://127.0.0.1:2023/openai/chat/completion"
data = {"prompt": "什么是python"}
response = session.post(url, json=data, stream=True)
for line in response:
    if line:
        # 处理流式数据
        print(line.decode('utf-8'), end='')
print('\n')

url = "http://127.0.0.1:2023/common/close"
response = session.get(url)
print(response.text)

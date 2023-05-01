# ThinkChat-server
## ThinkChat是一个基于OpenAI接口的聊天机器人，该项目目的为ThinkChat开发服务端

## 启动之前
1、准备好你的[openai key](https://platform.openai.com/account/api-keys)  

2、有一个运行redis的服务器  

3、安装依赖```pip install -r requirements.txt```

## 启动项目
执行命令```python run.py```

## 接口说明
```/common/connect```  
用于连接服务器，设置对话参数，需要以json的形式携带以下参数
```json
{
  "ChatCompletionConfig": {
    "model": "gpt-3.5-turbo",
    "temperature": 1,
    "n": 1,
    "stream": true,
    "stop": "",
    "max_tokens": 2048,
    "presence_penalty": 0,
    "frequency_penalty": 0
  },
  "ImageConfig": {
    "n": 1,
    "size": "1024x1024"
  },
  "max_context_size": 5,
  "auto_modify_cons": true,
  "openai_key": "openai_key"
}
```

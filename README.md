# ThinkChat-server
## ThinkChat是一个基于OpenAI接口的聊天机器人，该项目目的为ThinkChat开发服务端

## 启动之前
1、准备好你的[openai key](https://platform.openai.com/account/api-keys)  

2、有一个运行redis的服务器  

3、安装依赖```pip install -r requirements.txt```

## 启动项目
执行命令```python run.py```

## 接口说明
```/common/connect``` ```post```  
用于连接服务器，设置对话参数，需要以json的形式携带以下参数，同时服务器会在redis种持久化一个session来储存这些配置，**应该在调用其他接口之前首先调用该接口，否则会被拦截**
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
```max_context_size``` 代表系统每次发送请求携带的上下文数量
```auto_modify_cons``` 代表系统在运行过程是否自动调整```conversations```的大小  
其余参数的具体含义参考[OpenAI API官网](https://platform.openai.com/docs/api-reference)
  
```/common/close``` ```get```  
关闭连接，服务器会删除持久化在redis中的session  
  
```/common/select/record``` ```post```
用于选择当前对话的记录  
参数如下：  
```json
{"name": "record name"}
```

```/common/all/records``` ```get```
返回所有聊天记录的名称  
  
```/common/all/data/<record>``` ```get```
返回名为record的聊天记录中的所有内容 
  
```/openai/```
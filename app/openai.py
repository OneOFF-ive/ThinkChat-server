import json
from flask import session, request, Blueprint, Response, stream_with_context
from openai import InvalidRequestError
from openai.error import APIConnectionError
from lib.ApiBuilder import ApiBuilder
from app import redis_client

bp = Blueprint("openai", __name__, url_prefix='/openai')


@bp.route("/chat/completion", methods=["post"])
def ChatCompletion():
    data = request.json
    prompt = data.get("prompt")

    config = session.get('config')
    openai_key = config.openai_key
    chatCompletionConfig = config.chatCompletionConfig

    msg = {"role": "user", "content": prompt}
    key = openai_key + '_' + session.get("records_name")

    str_list = redis_client.lrange(key, -config.max_context_size + 1, -1)
    dict_list = [json.loads(item) for item in str_list]
    dict_list = dict_list[::-1]
    dict_list.append(msg)

    def generate_response(r):
        content = ''
        for chunk in r:
            chunk_message = chunk['choices'][0]['delta']
            chunk_content = chunk_message.get('content', '')
            content = content + chunk_content
            yield chunk_content
        answer = {"role": "assistant", "content": content}
        redis_client.lpush(key, json.dumps(answer))

    res = "unknown error"
    while True:
        try:
            completion = ApiBuilder.ChatCompletion(openai_key, dict_list, chatCompletionConfig)
            redis_client.lpush(key, json.dumps(msg))
            if chatCompletionConfig.stream:
                res = Response(stream_with_context(generate_response(completion)), content_type='text/plain')
            else:
                res = completion.choices[0]["message"]["content"]

            if config.auto_modify_cons:
                config.max_context_size = config.max_context_size + 2
            break
        except InvalidRequestError:
            if config.max_context_size > 2 and config.auto_modify_cons:
                config.max_context_size = int(config.max_context_size / 2)
                continue
            else:
                res = "invalid request"
                break
        except APIConnectionError or TimeoutError:
            res = "time out"
            break

    return res

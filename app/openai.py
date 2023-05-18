from flask import session, request, Blueprint, Response, stream_with_context
from openai import InvalidRequestError
from openai.error import APIConnectionError

from app import app
from lib.ApiBuilder import ApiBuilder

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

    db = app.config['db']

    def generate_response(r):
        content = ''
        for chunk in r:
            chunk_message = chunk['choices'][0]['delta']
            chunk_content = chunk_message.get('content', '')
            content = content + chunk_content
            if chunk_content != "":
                for char in chunk_content:
                    yield char.encode("utf-16")
        res_data = {"role": "assistant", "content": content}
        db.setData(key, res_data)

    res = "server error"
    while True:
        try:
            dict_list = db.getData(key, config.max_context_size - 1)
            dict_list.append(msg)
            completion = ApiBuilder.ChatCompletion(openai_key, dict_list, chatCompletionConfig)
            db.setData(key, msg)
            if chatCompletionConfig.stream:
                res = Response(stream_with_context(generate_response(completion)))
            else:
                res = completion.choices[0]["message"]["content"]
                answer = {"role": "assistant", "content": res}
                db.setData(key, answer)

            if config.auto_modify_cons:
                config.max_context_size = config.max_context_size + 2
            break
        except InvalidRequestError:
            if config.max_context_size > 1 and config.auto_modify_cons:
                config.max_context_size = int(config.max_context_size / 2)
                continue
            else:
                res = "invalid request"
                break
        except APIConnectionError or TimeoutError:
            res = "time out"
            break

    return res


@bp.route("image", methods=['post'])
def image():
    data = request.json
    prompt = data.get("prompt")
    config = session.get('config')
    openai_key = config.openai_key
    imageConfig = config.imageConfig

    try:
        return ApiBuilder.Image(openai_key, prompt, imageConfig)["data"][0]["url"]
    except APIConnectionError or TimeoutError:
        return "time out"
    except InvalidRequestError:
        return "invalid request"

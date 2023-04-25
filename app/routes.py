import json

from flask import make_response, session, request, jsonify

from app import app, redis_client
from lib.config import ChatCompletionConfig, ImageConfig, Config


@app.route("/connect", methods=['post'])
def connect():
    print(request.headers)
    json_data = request.json
    chatCompletionConfig = ChatCompletionConfig(**json_data.get("ChatCompletionConfig"))
    imageConfig = ImageConfig(**json_data.get("ImageConfig"))
    config = Config(chatCompletionConfig=chatCompletionConfig,
                    imageConfig=imageConfig,
                    max_context_size=json_data.get("max_context_size"),
                    auto_modify_cons=json_data.get("auto_modify_cons"))
    session["config"] = config
    return "connected"


@app.route("/test")
def test():
    print(request.headers)
    config = session.get('config')
    return config.__dict__


@app.route("/close")
def close():
    print(request.headers)
    session.clear()
    return "close"


@app.errorhandler(404)
def page_not_found(error):
    return "404"

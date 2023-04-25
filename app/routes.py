import json

from flask import make_response, session, request

from app import app, redis_client
from lib.config import ChatCompletionConfig, ImageConfig, Config


@app.route("/connect")
def connect():
    data = request.data
    json_data = json.loads(data)
    chatCompletionConfig = ChatCompletionConfig(**json_data.get("ChatCompletionConfig"))
    imageConfig = ImageConfig(**json_data.get("ImageConfig"))
    config = Config(chatCompletionConfig=chatCompletionConfig,
                    imageConfig=imageConfig,
                    max_context_size=json_data.get("max_context_size"),
                    auto_modify_cons=json_data.get("auto_modify_cons"))
    session["config"] = config
    return "connect"


@app.route("/test")
def test():
    return session.get("config")


@app.route("/close")
def close():
    session.clear()
    return "close"

@app.errorhandler(404)
def page_not_found(error):
    return "404"

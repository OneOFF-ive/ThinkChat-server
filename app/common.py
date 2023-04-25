from flask import session, request, Blueprint

from lib.config import ChatCompletionConfig, ImageConfig, Config

bp = Blueprint("common", __name__, url_prefix='/common')


@bp.route("/connect", methods=['post'])
def connect():
    json_data = request.json
    chatCompletionConfig = ChatCompletionConfig(**json_data.get("ChatCompletionConfig"))
    imageConfig = ImageConfig(**json_data.get("ImageConfig"))
    config = Config(chatCompletionConfig=chatCompletionConfig,
                    imageConfig=imageConfig,
                    max_context_size=json_data.get("max_context_size"),
                    auto_modify_cons=json_data.get("auto_modify_cons"))
    session["config"] = config
    return "connected"


@bp.route("/test")
def test():
    config = session.get('config')
    return config.__dict__


@bp.route("/close")
def close():
    session.clear()
    return "close"

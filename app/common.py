from flask import session, request, Blueprint
from lib.config import ChatCompletionConfig, ImageConfig, Config
from app import redis_client, app

bp = Blueprint("common", __name__, url_prefix='/common')


@bp.route("/connect", methods=['post'])
def connect():
    json_data = request.json
    chatCompletionConfig = ChatCompletionConfig(**json_data.get("ChatCompletionConfig"))
    imageConfig = ImageConfig(**json_data.get("ImageConfig"))
    config = Config(chatCompletionConfig=chatCompletionConfig,
                    imageConfig=imageConfig,
                    max_context_size=json_data.get("max_context_size"),
                    auto_modify_cons=json_data.get("auto_modify_cons"),
                    openai_key=json_data.get("openai_key"))
    session["config"] = config
    return "connected"


@bp.route("/select/record", methods=['post'])
def selectRecord():
    json_data = request.json
    name = json_data.get("name")
    session["records_name"] = name
    return name


@bp.route("/all/records", methods=['get'])
def allRecords():
    openai_key = session.get('config').openai_key
    keys = redis_client.keys(openai_key + "*")
    key_list = [key.decode('utf-8').replace(openai_key + '_', '', 1) for key in keys]
    return key_list


@bp.route("/all/data/<record>", methods=['get'])
def allData(record):
    openai_key = session.get('config').openai_key
    db = app.config['db']
    key = openai_key + "_" + record
    data = db.getAllData(key)
    return data

@bp.route("/close")
def close():
    session.clear()
    print("closed")
    return "closed"

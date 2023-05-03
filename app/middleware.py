from flask import request, session

from app import app


@app.before_request
def before_request():
    path = request.path
    if path == "/common/connect" or path == "/common/close":
        return
    else:
        if session.get("config") is None:
            return "not connect"
        if path == "/openai/chat/completion":
            if session.get("records_name") is None:
                return "not select record"
            else:
                return


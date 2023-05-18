from app import app
from flask import request, session


@app.before_request
def before_request():
    path = request.path
    if path == "/common/connect" or path == "/common/close":
        return
    else:
        if session.get("config") is None:
            print("not connect")
            return "not connect"
        if session.get("records_name") is None and path is not "/common/select/record":
            print("not select record")
            return "not select record"

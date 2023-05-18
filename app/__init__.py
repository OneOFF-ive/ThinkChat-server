from flask import Flask
from flask_session import Session

from lib.DataController import DataController, redis_client

app = Flask(__name__)
app.secret_key = 'my_secret_key'
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = redis_client
app.config['PERMANENT_SESSION_LIFETIME'] = 1800
app.config['db'] = DataController()
Session(app)

from app import common, openai

app.register_blueprint(common.bp)
app.register_blueprint(openai.bp)

from app import middleware

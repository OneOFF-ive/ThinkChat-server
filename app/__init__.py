from flask import Flask
from instance import redis_conf
from flask_session import Session
from redis import Redis
from lib.DataController import DataController

app = Flask(__name__)
app.secret_key = 'my_secret_key'
redis_client = Redis(host=redis_conf.redis_host,
                     port=redis_conf.redis_port,
                     password=redis_conf.redis_password,
                     db=redis_conf.redis_db)
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = redis_client
app.config['db'] = DataController()
Session(app)

from app import common, openai

app.register_blueprint(common.bp)
app.register_blueprint(openai.bp)

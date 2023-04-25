from flask import Flask
from flask_redis import FlaskRedis
from instance import redis_conf
from flask_session import Session
from redis import Redis

app = Flask(__name__)
app.secret_key = 'my_secret_key'
app.config['REDIS_URL'] = redis_conf.redis_url
redis_client = FlaskRedis(app)
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = Redis(host=redis_conf.redis_host,
                                    port=redis_conf.redis_port,
                                    password=redis_conf.redis_password,
                                    db=redis_conf.redis_db)
Session(app)

from app import common

app.register_blueprint(common.bp)

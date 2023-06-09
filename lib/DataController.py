import json

from redis import Redis

from instance import redis_conf

redis_client = Redis(host=redis_conf.redis_host,
                     port=redis_conf.redis_port,
                     password=redis_conf.redis_password,
                     db=redis_conf.redis_db)


class DataController:
    def __init__(self):
        self.db = redis_client

    def getData(self, key, num):
        str_list = self.db.lrange(key, -num, -1)
        dict_list = [json.loads(item) for item in str_list]
        dict_list = dict_list[::-1]
        return dict_list

    def setData(self, key, msg):
        self.db.lpush(key, json.dumps(msg))

    def getAllData(self, key):
        str_list = self.db.lrange(key, 0, -1)
        dict_list = [json.loads(item) for item in str_list]
        dict_list = dict_list[::-1]
        return dict_list

# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 12:37:57 2016

@author: Zhao Cheng
"""
from datetime import datetime
import configparser
import redis
import json


class RedisDB(object):
    def __init__(self, rediscfg='/redisdb.cfg'):
        self.rediscfg = rediscfg
        config = configparser.ConfigParser()
        with open(self.rediscfg, 'r') as cfgfile:
            config.read_file(cfgfile)
            self.cfghost = config.get('SERVER', 'host')
            self.cfgport = config.get('SERVER', 'port')
            self.cfglist = config.get('SERVER', 'list')

    def connect(self):
        pool = redis.ConnectionPool(host=self.cfghost, port=self.cfgport, db=0)
        r = redis.Redis(connection_pool=pool)
        return r

    def pop_stream(self, callback_func=lambda x: print(x)):
        r = self.connect()
        num = r.llen(self.cfglist)
        while True:
            if num > 0:
                data = r.rpop(self.cfglist).decode('utf-8')
                callback_func(json.loads(data))
                print(num)
            num = r.llen(self.cfglist)

    def push(self, dictdata):
        r = self.connect()
        if isinstance(dictdata, dict):
            print('TIME:', datetime.now())
            print("DATA:", dictdata)
            print("NUM:", r.lpush(self.cfglist, json.dumps(dictdata)))
        return None


def callback_redis(dictdata):
    redisdb = RedisDB()
    redisdb.push(dictdata)
    return None


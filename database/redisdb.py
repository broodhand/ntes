# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 12:37:57 2016

@author: Zhao Cheng
"""

import configparser
import redis
import json


class RedisDB(object):
    def __init__(self, rediscfg='database/redisdb.cfg'):
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

    def popdata(self,callback_func=lambda x: print(x)):
        r = self.connect()
        num = r.llen(self.cfglist)
        while True:
            if num > 0:
                callback_func(json.loads(r.rpop(self.cfglist)))
                print(num)
            num = r.llen(self.cfglist)


def rediscallback(dictdata):
    redisdb = RedisDB()
    r = redisdb.connect()
    if isinstance(dictdata, dict):
        print("DATA:", dictdata)
        print("NUM:", r.lpush(redisdb.cfglist, json.dumps(dictdata)))

    return None

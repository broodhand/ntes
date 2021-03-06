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
    def __init__(self, rediscfg='redisDB.cfg'):
        self.rediscfg = rediscfg
        config = configparser.ConfigParser()
        with open(self.rediscfg, 'r') as cfgfile:
            config.read_file(cfgfile)
            self.cfghost = config.get('REDIS', 'host')
            self.cfgport = config.get('REDIS', 'port')
            self.cfglist = config.get('REDIS', 'list')

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

    def pop_cachestream(self, callback_func=lambda x: print(x), cachenum=500, cacheseconds=60):
        from datastructure import Cache
        from datetime import datetime
        r = self.connect()
        num = r.llen(self.cfglist)
        cache = Cache(cachenum, cacheseconds)
        proctime = datetime.now()
        while 1:
            if num > 0:
                data = r.rpop(self.cfglist).decode('utf-8')
                cache.push(json.loads(data))
                tmpdata = cache.pop()
                if tmpdata:
                    callback_func(data)
                proctime = datetime.now()
            elif (datetime.now() - proctime).seconds > cacheseconds:
                tmpdata = cache.pop()
                if tmpdata:
                    callback_func(data)
                proctime = datetime.now()
            num = r.llen(self.cfglist)

    def push(self, dictdata):
        r = self.connect()
        if isinstance(dictdata, dict):
            print('TIME:', datetime.now())
            print("DATA:", dictdata)
            print("NUM:", r.lpush(self.cfglist, json.dumps(dictdata)))


def callback_redis(datas):
    redisdb = RedisDB()
    if isinstance(datas, dict):
        redisdb.push(datas)
    if isinstance(datas, tuple) or isinstance(datas, list):
        for data in datas:
            if isinstance(data, dict):
                redisdb.push(data)
    return redisdb.connect().llen(redisdb.cfglist)


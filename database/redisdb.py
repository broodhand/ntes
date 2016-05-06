# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 12:37:57 2016

@author: Zhao Cheng
"""

import configparser
import redis
import json


class RedisDB(object):
    def __init__(self, rediscfg='rediscfg'):
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


def redis_callback(dictdata):
    redisdb = RedisDB()
    r = redisdb.connect()
    if isinstance(dictdata,dict):
        try:
            r.lpush(redisdb.cfglist, json.dumps(dictdata))
        print(r.llen(redisdb.cfglist))
    return None

# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 12:37:57 2016

@author: Administrator
"""
"""
from nets import NtesTickData
import redis
import json

def callback(data):
    r.lpush('ntes', json.dumps(data))

r = redis.StrictRedis(host='spbgcapital.f3322.net', port=6379, db=0)
NtesTickData('204001').value_stream(3, callback)

''''''

'''
while True:
    data = ntesdata('150201').get()
    print(r.rpush('test',data))
    time.sleep(0.05)
'''

"""
import configparser
import redis
import logging

class RedisDB(object):
    def __init__(self,rediscfg = 'rediscfg'):
        self.rediscfg = rediscfg

    def connect(self):
        config = configparser.ConfigParser()
        with open(self.rediscfg, 'r') as cfgfile:
            config.read_file(cfgfile)
            cfghost = config.get('SERVER', 'host')
            cfgport = config.get('SERVER', 'port')
        pool = redis.ConnectionPool(host=cfghost, port=cfgport, db=0)
        try:
            r = redis.Redis(connection_pool=pool)
        except Exception as e:
            logging.exception(e)
        return r

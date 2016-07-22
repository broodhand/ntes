# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 12:37:57 2016
@author: Zhao Cheng
__version__ = '0.0.1'
This is a set of orm to redis.
"""
import logging; logging.basicConfig(level=logging.DEBUG)
from . import api
from .error import RedisKeyError


class Key(object):
    def __init__(self, key_name, **kwargs):
        if api.exists(key_name, **kwargs):
            self.name = key_name
            self.cfg_connect = kwargs
        else:
            raise RedisKeyError('Key not exists')

    @property
    def exists(self):
        return api.exists(self.name, **self.cfg_connect)

    @property
    def type(self):
        return api.keytype(self.name, **self.cfg_connect)

    @classmethod
    def delkey(cls, *key, **kwargs):
        return api.delkey(*key, **kwargs)

    @classmethod
    def keys(cls, **kwargs):
        return api.keys(**kwargs)


class Set(object):
    def __init__(self, key_name, **kwargs):
        self.key_name = key_name
        self.redis_cfg = kwargs

    @property
    def members(self):
        return api.smembers(self.key_name, **self.redis_cfg)

    def ismember(self, value):
        return api.sismember(self.key_name, value, **self.redis_cfg)




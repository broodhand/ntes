# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 11:02:14 2016
__version__ = '0.0.2'
@author:Zhao Cheng
"""
import logging; logging.basicConfig(level=logging.DEBUG)
import redisDB.api


class Set(set):
    def __init__(self, *args, **kwargs):
        super(Set, self).__init__(*args, **kwargs)

    def redis_update(self, key_name, **kwargs):
        return redisDB.api.sadd(key_name, *tuple(self), **kwargs)

    def redis_mapping(self, key_name, **kwargs):
        if not redisDB.api.exists(key_name):
            return redisDB.api.sadd(key_name, *tuple(self), **kwargs)
        else:
            redisDB.api.delkey(key_name, **kwargs)
            return redisDB.api.sadd(key_name, *tuple(self), **kwargs)

    def redis_mappingnx(self, key_name, **kwargs):
        if not redisDB.api.exists(key_name):
            return redisDB.api.sadd(key_name, *tuple(self), **kwargs)
        else:
            return False


class Dict(dict):
    def __init__(self, *args, **kwargs):
        super(Dict, self).__init__(*args, **kwargs)

    def redis_update(self, key_name, **kwargs):
        return redisDB.api.hmset(key_name, self, **kwargs)

    def redis_mapping(self, key_name, **kwargs):
        if not redisDB.api.exists(key_name):
            return redisDB.api.hmset(key_name, self, **kwargs)
        else:
            redisDB.api.delkey(key_name, **kwargs)
            return redisDB.api.hmset(key_name, self, **kwargs)

    def redis_mappingnx(self, key_name, **kwargs):
        if not redisDB.api.exists(key_name):
            return redisDB.api.hmset(key_name, self, **kwargs)
        else:
            return False


class Str(str):
    def __init__(self, value):
        super(Str, self).__init__()
        self = value

    def redis_set(self, key_name, **kwargs):
            return redisDB.api.set(key_name, self, **kwargs)

    def redis_mappingnx(self, key_name, **kwargs):
            return redisDB.api.set(key_name, self, nx=True, **kwargs)



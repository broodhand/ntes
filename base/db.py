# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 11:02:14 2016
__version__ = '0.0.3'
@author:Zhao Cheng
"""
import redisDB.api


class Set(set):
    def __init__(self, *args, **kwargs):
        super(Set, self).__init__(*args, **kwargs)

    def redis_update(self, key_name, **kwargs_redis):
        return redisDB.api.sadd(key_name, *tuple(self), **kwargs_redis)

    def redis_update_pipeline(self, key_name, pipeline):
        return pipeline.sadd(key_name, *tuple(self))

    def redis_mapping(self, key_name, **kwargs_redis):
        redisDB.api.delkey(key_name, **kwargs_redis)
        return redisDB.api.sadd(key_name, *tuple(self), **kwargs_redis)

    def redis_mapping_pipeline(self, key_name, pipeline):
        return pipeline.delete(key_name).sadd(key_name, *tuple(self))

    def redis_mappingnx(self, key_name, **kwargs_redis):
        if not redisDB.api.exists(key_name, **kwargs_redis):
            return redisDB.api.sadd(key_name, *tuple(self), **kwargs_redis)
        else:
            return False


class Dict(dict):
    def __init__(self, *args, **kwargs):
        super(Dict, self).__init__(*args, **kwargs)

    def redis_update(self, key_name, **kwargs_redis):
        return redisDB.api.hmset(key_name, self, **kwargs_redis)

    def redis_update_pipeline(self, key_name, pipeline):
        return pipeline.hmset(key_name, self)

    def redis_mapping(self, key_name, **kwargs_redis):
        redisDB.api.delkey(key_name, **kwargs_redis)
        return redisDB.api.hmset(key_name, self, **kwargs_redis)

    def redis_mapping_pipeline(self, key_name, pipeline):
        return pipeline.delete(key_name).hmset(key_name, self)

    def redis_mappingnx(self, key_name, **kwargs_redis):
        if not redisDB.api.exists(key_name, **kwargs_redis):
            return redisDB.api.hmset(key_name, self, **kwargs_redis)
        else:
            return False

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value


class Str(str, object):
    def __init__(self, *args, **kwargs):
        super(Str, self).__init__(*args, **kwargs)

    def redis_set(self, key_name, **kwargs_redis):
            return redisDB.api.set(key_name, self, **kwargs_redis)

    def redis_set_pipeline(self, key_name, pipeline):
        return pipeline.set(key_name, self)

    def redis_mappingnx(self, key_name, **kwargs_redis):
            return redisDB.api.set(key_name, self, nx=True, **kwargs_redis)

    def redis_mappingnx_pipeline(self, key_name, pipeline):
        return pipeline.set(key_name, self, nx=True)
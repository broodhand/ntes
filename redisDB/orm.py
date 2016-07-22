# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 12:37:57 2016
@author: Zhao Cheng
__version__ = '0.0.3'
This is a set of orm to redis.
"""
import logging; logging.basicConfig(level=logging.DEBUG)
from . import api
from .error import RedisKeyError


def get_set_key(value, **kwargs):
    key = None
    if isinstance(value, str):
        key = Set(value, **kwargs).key
    elif isinstance(value, Set):
        key = value.key
    if key:
        return key
    else:
        raise RedisKeyError("Must input string or class Set")


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
        key = Key(key_name)
        if key.type == 'set':
            self.key = key
            self.redis_cfg = kwargs
        else:
            raise RedisKeyError("Key's type must be set")

    def __repr__(self):
        return str(self.members)

    @property
    def members(self):
        return api.smembers(self.key.name, **self.redis_cfg)

    def ismember(self, member):
        return api.sismember(self.key.name, member, **self.redis_cfg)

    def add(self, *members):
        return api.sadd(self.key.name, *members, **self.redis_cfg)

    @property
    def card(self):
        return api.scard(self.key.name, **self.redis_cfg)

    def diff(self, diff_set):
        diff_key = get_set_key(diff_set, **self.redis_cfg)
        return api.sdiff(self.key, diff_key.name, **self.redis_cfg)

    def diffstore(self, store_key_name, diff_set):
        diff_key = get_set_key(diff_set, **self.redis_cfg)
        return api.sdiffstore(store_key_name, self.key.name, diff_key.name, **self.redis_cfg)

    def inter(self, inter_set):
        inter_key = get_set_key(inter_set, **self.redis_cfg)
        return api.sdiff(self.key, inter_key.name, **self.redis_cfg)

    def interstore(self, store_key_name, inter_set):
        inter_key = get_set_key(inter_set, **self.redis_cfg)
        return api.sinterstore(store_key_name, self.key.name, inter_key.name, **self.redis_cfg)

    def move(self, moveto_set, member):
        moveto_key = get_set_key(moveto_set, **self.redis_cfg)
        return api.smove(self.key.name, moveto_key.name, member, **self.redis_cfg)

    def pop(self):
        return api.spop(self.key.name, **self.redis_cfg)

    def randmember(self, count=0):
        return api.srandmember(self.key.name, count, **self.redis_cfg)

    def rem(self, member):
        return api.srem(self.key.name, member, **self.redis_cfg)

    def union(self, union_set):
        union_key = get_set_key(union_set, **self.redis_cfg)
        return api.sunion(self.key.name, union_key.name, **self.redis_cfg)

    def unionstore(self, store_key_name, union_set):
        union_key = get_set_key(union_set, **self.redis_cfg)
        return api.sunionstore(store_key_name, self.key.name, union_key.name, **self.redis_cfg)

    def scan(self, cursor, *args):
        return api.sscan(self.key.name, cursor, *args, **self.redis_cfg)

    @classmethod
    def sadd(cls, key_name, *members, **redis_cfg):
        return api.sadd(key_name, *members, **redis_cfg)


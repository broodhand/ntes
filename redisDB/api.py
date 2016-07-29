"""
Created on Wed Mar 23 12:37:57 2016
@author: Zhao Cheng
__version__ = '0.0.5'
This is a set of api library for using class redis.StrictRedis
"""
from .connect import with_connect


# Following are APIs for basic***************************************************************************
@with_connect
def pipeline(**kwargs_redis):
    return kwargs_redis['client'].pipeline()


@with_connect
def flushall(**kwargs_redis):
    return kwargs_redis['client'].flushall()


@with_connect
def flushdb(**kwargs_redis):
    return kwargs_redis['client'].flushdb()


@with_connect
def dbsize(**kwargs_redis):
    return kwargs_redis['client'].dbsize()


@with_connect
def info(**kwargs_redis):
    return kwargs_redis['client'].info()


# Following are APIs for type key************************************************************************
@with_connect
def exists(key, **kwargs_redis):
        return kwargs_redis['client'].exists(key)


@with_connect
def keytype(key, **kwargs_redis):
    return kwargs_redis['client'].type(key)


@with_connect
def delkey(*key, **kwargs_redis):
    return kwargs_redis['client'].delete(*key)


@with_connect
def keys(**kwargs_redis):
    return kwargs_redis['client'].keys()


# Following are APIs for type set*************************************************************************
@with_connect
def smembers(key_name, **kwargs_redis):
    return kwargs_redis['client'].smembers(key_name)


@with_connect
def sismember(key_name, member, **kwargs_redis):
    return kwargs_redis['client'].sismember(key_name, member)


@with_connect
def sadd(key_name, *members, **kwargs_redis):
    return kwargs_redis['client'].sadd(key_name, *members)


@with_connect
def scard(key_name, **kwargs_redis):
    return kwargs_redis['client'].scard(key_name)


@with_connect
def sdiff(key_name, diff_key_name, **kwargs_redis):
    return kwargs_redis['client'].sdiff(key_name, diff_key_name)


@with_connect
def sdiffstore(store_key_name, key_name, diff_key_name, **kwargs_redis):
    return kwargs_redis['client'].sdiffstore(store_key_name, key_name, diff_key_name)


@with_connect
def sinter(key_name, inter_key_name, **kwargs_redis):
    return kwargs_redis['client'].sinter(key_name, inter_key_name)


@with_connect
def sinterstore(store_key_name, key_name, inter_key_name, **kwargs_redis):
    return kwargs_redis['client'].sinterstore(store_key_name, key_name, inter_key_name)


@with_connect
def smove(key_name, move_key_name, member, **kwargs_redis):
    return kwargs_redis['client'].smove(key_name, move_key_name, member)


@with_connect
def spop(key_name, **kwargs_redis):
    return kwargs_redis['client'].spop(key_name)


@with_connect
def srandmember(key_name, count=0, **kwargs_redis):
    return kwargs_redis['client'].srandmember(key_name, count)


@with_connect
def srem(key_name, *member, **kwargs_redis):
    return kwargs_redis['client'].srem(key_name, *member)


@with_connect
def sunion(key_name, union_key_name, **kwargs_redis):
    return kwargs_redis['client'].sunion(key_name, union_key_name)


@with_connect
def sunionstore(store_key_name, key_name, union_key_name, **kwargs_redis):
    return kwargs_redis['client'].sunionstore(store_key_name, key_name, union_key_name)


@with_connect
def sscan(key_name, cursor, *args, **kwargs_redis):
    return kwargs_redis['client'].sscan(key_name, cursor, *args)


@with_connect
def sscan_iter(key_name, *args, **kwargs_redis):
    return kwargs_redis['client'].sscan_iter(key_name, *args)


# Following are APIs for type hash*************************************************************************
@with_connect
def hset(key_name, field_name, field_value, **kwargs_redis):
    return kwargs_redis['client'].hset(key_name, field_name, field_value)


@with_connect
def hsetnx(key_name, field_name, field_value, **kwargs_redis):
    return kwargs_redis['client'].hsetnx(key_name, field_name, field_value)


@with_connect
def hmset(key_name, dict_mapping, **kwargs_redis):
    return kwargs_redis['client'].hmset(key_name, dict_mapping)


@with_connect
def hdel(key_name, field_name1, *filed_names, **kwargs_redis):
    return kwargs_redis['client'].hdel(key_name, field_name1, *filed_names)


@with_connect
def hget(key_name, field_name, **kwargs_redis):
    return kwargs_redis['client'].hget(key_name, field_name)


@with_connect
def hmget(key_name, field_name, *field_names, **kwargs_redis):
    return kwargs_redis['client'].hmget(key_name, field_name, *field_names)


@with_connect
def hexists(key_name, field_name, **kwargs_redis):
    return kwargs_redis['client'].hexists(key_name, field_name)


@with_connect
def hlen(key_name, **kwargs_redis):
    return kwargs_redis['client'].hlen(key_name)


@with_connect
def hkeys(key_name, **kwargs_redis):
    return kwargs_redis['client'].hkeys(key_name)


@with_connect
def hvals(key_name, **kwargs_redis):
    return kwargs_redis['client'].hvals(key_name)


@with_connect
def hgetall(key_name, **kwargs_redis):
    return kwargs_redis['client'].hgetall(key_name)


@with_connect
def hincrby(key_name, field_name, incr, **kwargs_redis):
    return kwargs_redis['client'].hincrby(key_name, field_name, incr)


@with_connect
def hincrbyfloat(key_name, filed_name, incr, **kwargs_redis):
    return kwargs_redis['client'].hincrbyfloat(key_name, filed_name, incr)


@with_connect
def hscan(key_name, cursor, *args, **kwargs_redis):
    return kwargs_redis['client'].hscan(key_name, cursor, *args)


@with_connect
def hscan_iter(key_name, *args, **kwargs_redis):
    return kwargs_redis['client'].hscan_iter(key_name, *args)


# Following are APIs for type str**************************************************************************
@with_connect
def set(key_name, value, ex=None, px=None, nx=False, xx=False, **kwargs_redis):
    return kwargs_redis['client'].set(key_name, value, ex, px, nx, xx)


@with_connect
def get(key_name, **kwargs_redis):
    return kwargs_redis['client'].get(key_name)

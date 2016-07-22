"""
Created on Wed Mar 23 12:37:57 2016
@author: Zhao Cheng
__version__ = '0.0.3'
This is a set of api library for using class redis.StrictRedis
"""
from .connect import with_connect


# Following are APIs for type key************************************************************************
@with_connect
def exists(client_with_connect, key, **kwargs_with_connect):
        return client_with_connect.exists(key)


@with_connect
def keytype(client_with_connect, key, **kwargs_with_connect):
    return client_with_connect.type(key)


@with_connect
def delkey(client_with_connect, *key, **kwargs_with_connect):
    return client_with_connect.delete(*key)


@with_connect
def keys(client_with_connect,**kwargs_with_connect):
    return client_with_connect.keys()


# Following are APIs for type set*************************************************************************
@with_connect
def smembers(client_with_connect, key_name, **kwargs_with_connect):
    return client_with_connect.smembers(key_name)


@with_connect
def sismember(client_with_connect, key_name, member, **kwargs_with_connect):
    return client_with_connect.sismember(key_name, member)


@with_connect
def sadd(client_with_connect, key_name, *members, **kwargs_with_connect):
    return client_with_connect.sadd(key_name, *members)


@with_connect
def scard(client_with_connect, key_name, **kwargs_with_connect):
    return client_with_connect.scard(key_name)


@with_connect
def sdiff(client_with_connect, key_name, diff_key_name, **kwargs_with_connect):
    return client_with_connect.sdiff(key_name, diff_key_name)


@with_connect
def sdiffstore(client_with_connect, store_key_name, key_name, diff_key_name, **kwargs_with_connect):
    return client_with_connect.sdiffstore(store_key_name, key_name, diff_key_name)


@with_connect
def sinter(client_with_connect, key_name, inter_key_name, **kwargs_with_connect):
    return client_with_connect.sinter(key_name, inter_key_name)


@with_connect
def sinterstore(client_with_connect, store_key_name, key_name, inter_key_name, **kwargs_with_connect):
    return client_with_connect.sinterstore(store_key_name, key_name, inter_key_name)


@with_connect
def smove(client_with_connect, key_name, move_key_name, member, **kwargs_with_connect):
    return client_with_connect.smove(key_name, move_key_name, member)


@with_connect
def spop(client_with_connect, key_name, **kwargs_with_connect):
    return client_with_connect.spop(key_name)


@with_connect
def srandmember(client_with_connect, key_name, count=0, **kwargs_with_connect):
    return client_with_connect.srandmember(key_name, count)


@with_connect
def srem(client_with_connect, key_name, *member, **kwargs_with_connect):
    return client_with_connect.srem(key_name, *member)


@with_connect
def sunion(client_with_connect, key_name, union_key_name, **kwargs_with_connect):
    return client_with_connect.sunion(key_name, union_key_name)


@with_connect
def sunionstore(client_with_connect, store_key_name, key_name, union_key_name, **kwargs_with_connect):
    return client_with_connect.sunionstore(store_key_name, key_name, union_key_name)


@with_connect
def sscan(client_with_connect, key_name, cursor, *args, **kwargs_with_connect):
    return client_with_connect.sscan(key_name, cursor, *args)


# Following are APIs for type hash*************************************************************************

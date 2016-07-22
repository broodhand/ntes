"""
Created on Wed Mar 23 12:37:57 2016
@author: Zhao Cheng
__version__ = '0.0.2'
This is a set of api library for using class redis.StrictRedis
"""
from .connect import with_connect, RedisError
from .orm import Key


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


@with_connect
def smembers(client_with_connect, key_name, **kwargs_with_connect):
    key = Key(key_name)
    if key.type == 'set':
        return client_with_connect.smembers(key.name)
    else:
        raise RedisError("Have no key %s or key %s 's type is not set" % (key.name, key.name))


@with_connect
def sismember(client_with_connect, key_name, value, **kwargs_with_connect):
    key = Key(key_name)
    if key.type == 'set':
        return client_with_connect.sismember(key.name, value)
    else:
        raise RedisError("Have no key %s or key %s 's type is not set" % (key.name, key.name))


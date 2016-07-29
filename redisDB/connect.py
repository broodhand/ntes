# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 12:37:57 2016
@author: Zhao Cheng
__version__ = '0.2.1'
This is a set of api library for using Class redis.ConnectionPool().
"""
import redis
import functools
import threading
from .error import RedisError


def with_connection(**kwargs):
    """
    when func need args client,
    We can use "@with_connection(**kwargs)" auto pass redis client to func's kwarg client.
    example:
    @with_connection(db=1)
    def redis_info(client=None):
        return client.info()
    """
    def _decorator(func):
        @functools.wraps(func)
        def _wrapper(*args, **kw):
            with connection(**kwargs) as redis_connection:
                kw['client'] = redis_connection.client()
                return func(*args, **kw)
        return _wrapper
    return _decorator


def with_connect(func):
    """
    when func need arg client,
    We can use "@with_connection" auto pass redis client to func's first arg.
    example:
    @with_connection
    def redis_info(client,**kwarg):  # kwarg is redis.ConnectionPool's kwarg
        return client.info()
    """
    @functools.wraps(func)
    def _wrapper(*args, **kw):
        with connection(**kw) as redis_connection:
            kw['client'] = redis_connection.client()
            return func(*args, **kw)
    return _wrapper


class connection(threading.local):
    "This Class store redis.ConnectionPool() instance information."
    def __init__(self, **kwargs):
        "Create Class redis.ConnectionPool's instance."
        self._default = dict(max_connections=None, host='localhost', port=6379, db=0, password=None,
                             socket_timeout=None, socket_connect_timeout=None, socket_keepalive=False,
                             socket_keepalive_options=None, retry_on_timeout=False, encoding='utf-8',
                             encoding_errors='strict', decode_responses=True, socket_read_size=65536)
        self._kwargs = self._default.copy()
        self._kwargs.update(kwargs)
        self._pool = None
        self._client = None
        self._connect = False

    def connect(self):
        """
        To connect redis.
        :return:True(Success)
        """
        if self._connect is False:
            self._pool = redis.ConnectionPool(**self._kwargs)
            self._client = redis.StrictRedis(connection_pool=self._pool)
            self._connect = True
        else:
            raise RedisError('Already connect')
        return True

    def client(self):
        """
        get the client
        :return: Class redis.StrictRedis instance
        """
        if self._connect is True:
            return self._client
        else:
            raise RedisError('Need to connect redis first')

    def set_config(self, **kwargs):
        "Set the kwarg which pass to the Class redis.ConnectionPool"
        if self._connect is True:
            self._kwargs.update(kwargs)
            self._pool.disconnect()
            self._pool = redis.ConnectionPool(**self._kwargs)
            self._client = redis.StrictRedis(connection_pool=self._pool)
        else:
            raise RedisError('Need to connect first')
        return True

    def close(self):
        "Close the connection"
        if self._connect is True:
            self._pool.disconnect()
            self._pool = None
            self._client = None
            self._kwargs = self._default.copy()
            self._connect = False
        else:
            raise RedisError('Redis is not connected now.')
        return True

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


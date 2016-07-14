# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 12:37:57 2016
@author: Zhao Cheng

This is a set of api library for using Class redis.ConnectionPool().
"""
import logging;logging.basicConfig(level=logging.DEBUG)
import redis
import functools
import threading
from .error import RedisError

_redis = None  # Global variable to store instance of Class _Redis()


def with_redis(**kwargs):
    """
    for using "@with_redis"
    """
    def _decorator(func):
        @functools.wraps(func)
        def _wrapper(*args, **kw):
            with redis_client(**kwargs):
                return func(*args, **kw)
        return _wrapper
    return _decorator


def have_client():
    global _redis
    if _redis is not None:
        return True
    else:
        return False


def create_client(**kwargs):
    """
    Create a instance of Class _Redis().
    And store it in the global variable _redis.
    The kwargs will pass to the Class redis.ConnectionPool().
    :arg: max_connections=None Set max_connections,if > max_connections raise redis.ConnectionError
    :arg: host='localhost'
    :arg: port=6379
    :arg: db=0
    :arg: password=None
    :arg: socket_timeout=None tcp timeout
    :arg: encoding='utf-8'
    :arg: encoding_errors='strict'
    ...
    :return: True Success
    :return: None Fail
    >>> create_client()
    True
    >>> create_client()
    Traceback (most recent call last):
    ...
    redis.RedisError: Already create pool
    """
    global _redis
    if _redis is None:
        _redis = _Redis(**kwargs)
        return True
    else:
        raise RedisError('Already create redis')


def get_client():
    if have_client():
        global _redis
        return _redis.redis
    else:
        raise RedisError('Need to connect Redis')


def set_config(**kwargs):
    """
    Change the kwargs which pass to the Class redis.ConnectionPool().
    :arg: max_connections=None Set max_connections,if > max_connections raise redis.ConnectionError
    :arg: host='localhost'
    :arg: port=6379
    :arg: db=0
    :arg: password=None
    :arg: socket_timeout=None tcp timeout
    :arg: encoding='utf-8'
    :arg: encoding_errors='strict'
    ...
    :return: True Success
    :return: None Fail
    """
    global _redis
    if _redis is not None:
        _redis.set_config(**kwargs)
        logging.info('set config %s' % kwargs)
        return True
    else:
        raise RedisError('Need to create redis')


def select_db(db):
    """
    Change the redis database
    :param db: Redis's database number
    :return: True Success
    :return: None Fail
    """
    return set_config(db=db)


def set_timeout(s):
    """
    Change the socket timeout
    :param s: socket timeout
    :return: True Success
    :return: None Fail
    """
    return set_config(socket_connect_timeout=s)


def close_client():
    """
    close redis
    :return: True Success
    :return: None Fail
    """
    global _redis
    if _redis is not None:
        _redis.close()
    _redis = None
    logging.info('close redis client')
    return True


class _Redis(threading.local):
    "This Class store redis.ConnectionPool() instance information."
    def __init__(self, **kwargs):
        "Create Class redis.ConnectionPool's instance."
        self.default = dict(max_connections=None, host='localhost', port=6379, db=0,
                            password=None, socket_timeout=None, socket_connect_timeout=None,
                            socket_keepalive=False, socket_keepalive_options=None,
                            retry_on_timeout=False, encoding='utf-8', encoding_errors='strict',
                            decode_responses=False, socket_read_size=65536)
        self.kwargs = self.default.copy()
        self.kwargs.update(kwargs)
        self.pool = redis.ConnectionPool(**self.kwargs)
        self.redis = redis.StrictRedis(self.pool)

    def set_config(self, **config):
        "Set the kwarg which pass to the Class redis.ConnectionPool"
        if self.pool is not None:
            self.pool.disconnect()
            self.kwargs.update(config)
        self.pool = redis.ConnectionPool(**self.kwargs)
        self.redis = redis.StrictRedis(self.pool)
        logging.debug('set config %s' % config)
        return True

    def close(self):
        "Close the pool"
        if self.pool is not None:
            self.pool.disconnect()
        self.pool = None
        self.redis = None
        self.kwargs = self.default.copy()
        logging.debug('close pool')
        return True


class redis_client(object):
    """
    For using "with redis_client():"
    """
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __enter__(self):
        self.should_close = False

        if not have_client():
            if create_client(**self.kwargs):
                self.should_close = True
        else:
            if set_config(**self.kwargs):
                self.should_close = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.should_close:
            close_client()

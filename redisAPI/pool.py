# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 12:37:57 2016
@author: Zhao Cheng

This is a set of api library for using Class redis.ConnectionPool().
"""
import logging;logging.basicConfig(level=logging.DEBUG)
import redis
import functools
from .error import PoolError

_pool = None  # Global variable to store instance of Class _Pool()


def with_redis(**kwargs):
    """
    for using "@check_redis"
    """
    def _decorator(func):
        @functools.wraps(func)
        def _wrapper(*args, **kw):
            with redis_connection(**kwargs):
                return func(*args, **kw)
        return _wrapper
    return _decorator


def have_pool():
    global _pool
    if _pool is not None:
        return True
    else:
        return False


def create_pool(**kwargs):
    """
    Create a instance of Class _Pool().
    And store it in the global variable _pool.
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
    >>> create_pool()
    True
    >>> create_pool()
    Traceback (most recent call last):
    ...
    pool.PoolError: Already create pool
    """
    global _pool
    if _pool is None:
        _pool = _Pool(**kwargs)
        return True
    else:
        raise PoolError('Already create pool')


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
    global _pool
    if _pool is not None:
        _pool.set_config(**kwargs)
        logging.info('set config %s' % kwargs)
        return True
    else:
        raise PoolError('Need to create pool')


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
    return set_config(socket_timeout=s)


def close_pool():
    """
    close pool
    :return: True Success
    :return: None Fail
    """
    global _pool
    if _pool is not None:
        _pool.close()
    _pool = None
    logging.info('close pool')
    return True


class _Pool(object):
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

    def set_config(self, **config):
        "Set the kwarg which pass to the Class redis.ConnectionPool"
        if self.pool is not None:
            self.pool.disconnect()
            self.kwargs.update(config)
        self.pool = redis.ConnectionPool(**self.kwargs)
        logging.debug('set config %s' % config)
        return True

    def close(self):
        "Close the pool"
        if self.pool is not None:
            self.pool.disconnect()
        self.pool = None
        self.kwargs = self.default.copy()
        logging.debug('close pool')
        return True

    def redis(self):
        "Create Class redis.StrictRedis"
        if self.pool is not None:
            return redis.StrictRedis(connection_pool=self.pool)


class redis_connection(object):
    """
    For using "with redis_connection():"
    """
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __enter__(self):
        self.should_close = False

        if not have_pool():
            if create_pool(**self.kwargs):
                self.should_close = True
        else:
            if set_config(**self.kwargs):
                self.should_close = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.should_close:
            close_pool()

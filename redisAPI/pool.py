# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 12:37:57 2016

@author: Zhao Cheng
"""
import logging; logging.basicConfig(level=logging.DEBUG)
import redis

_pool = None


def create_pool(*args, **kwargs):
    global _pool
    if _pool is None:
        _pool = _Pool(*args, **kwargs)
    else:
        raise PoolError('Already create pool')


def set_config(**kwargs):
    global _pool
    if _pool is not None:
        _pool.set_config(**kwargs)
        logging.info('set config %s' % kwargs)
    else:
        raise PoolError('Need to create pool')


def select_db(db):
    set_config(db=db)


def set_timeout(s):
    set_config(socket_timeout=s)


def close_pool():
    global _pool
    if _pool is not None:
        _pool.close()
    _pool = None
    logging.info('close pool')


class _Pool(object):
    """
    redis connection pool class
    """
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.pool = redis.ConnectionPool(*self.args, **self.kwargs)

    def set_config(self, **config):
        if self.pool is not None:
            self.pool.disconnect()
        for k, v in config.items():
            self.kwargs[k] = v
        self.pool = redis.ConnectionPool(*self.args, **self.kwargs)
        logging.debug('set config %s' % config)

    def close(self):
        if self.pool is not None:
            self.pool.disconnect()
        self.pool = None
        logging.debug('close pool')

    def redis(self):
        if self.pool is not None:
            return redis.StrictRedis(connection_pool=self.pool)


class PoolError(Exception):
    pass

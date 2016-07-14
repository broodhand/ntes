# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 12:37:57 2016
@author: Zhao Cheng

Control the Class redis.StrictRedis
"""
import logging; logging.basicConfig(level=logging.DEBUG)
import threading
import functools
from .error import ClientError


def with_client(func):
    """
    for using @with_redis
    """
    @functools.wraps(func)
    def _wrapper(*args, **kw):
        from .pool import _pool
        if _pool is None:
            raise ClientError('Need to create pool')
        with _clientctx():
            return func(*args, **kw)
    return _wrapper


class _Client(threading.local):
    """
    This Class Create the instance of Class redis.Strict and save it in the self.redis.
    This Class is using Class threading.local for multiprocessing.
    """
    def __init__(self):
        self.redis = None

    def is_init(self):
        "Judge the initial condition of self.redis "
        return self.redis is not None

    def init(self):
        "Initialize the self.redis"
        from .pool import _pool
        self.redis = _pool.redis()
        logging.info('open redis redis...')

    def cleanup(self):
        "clean up self.redis"
        if self.is_init():
            self.redis = None

_client = _Client()  # _client is a global variable for saving Class _Client's instance.


class _clientctx(object):
    """
    For using "with _clientctx():" statement
    """
    def __enter__(self):
        global _client
        self.should_cleanup = False
        if not _client.is_init():
            _client.init()
            self.should_cleanup = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        global _client
        if self.should_cleanup:
            _client.cleanup()


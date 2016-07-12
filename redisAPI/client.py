# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 12:37:57 2016

@author: Zhao Cheng
"""
import logging; logging.basicConfig(level=logging.DEBUG)
import threading
import functools


def with_client(func):
    @functools.wraps(func)
    def _wrapper(*args, **kw):
        from .pool import _pool
        if _pool is None:
            raise ClientError('Need to create pool')
        with _clientctx():
            return func(*args, **kw)
    return _wrapper


class _Client(threading.local):
    def __init__(self):
        self.redis = None

    def is_init(self):
        return self.redis is not None

    def init(self):
        from .pool import _pool
        self.redis = _pool.redis()
        logging.info('open redis client...')

    def cleanup(self):
        if self.is_init():
            self.redis = None

_client = _Client()


class _clientctx(object):
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


class ClientError(Exception):
    pass

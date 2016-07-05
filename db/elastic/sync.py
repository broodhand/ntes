#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2016/6/30 10:58

@project: Grandet
@version: 0.99
@file: sync.py
@author: SPBG Co.,Ltd. ing / 北京正民惠浩投资管理有限公司 ing
@contact: ing@spbgcapital.com
@site: http://www.spbgcapital.net
"""
import logging; logging.basicConfig(level=logging.DEBUG)
import functools
import threading
from elasticsearch import Elasticsearch, helpers

engine = None


def _create_engine(url, **kw):
    global engine
    if engine is not None:
        raise DBError('Engine is already initialized.')
    engine = _Engine(url, **kw)
    logging.info('Init mysql engine <%s> ok.' % hex(id(engine)))


def init_engine():
    global engine
    engine = None


def create_engine(url, **kw):
    _create_engine(url, **kw)


def create_engine_cfgfile(file='sync.cfg', **kw):
    import configparser
    config = configparser.ConfigParser()
    with open(file, 'r') as cfgfile:
        config.read_file(cfgfile)
        url = config.get('ES', 'url')
    _create_engine(url, **kw)


def with_connection(func):
    @functools.wraps(func)
    def _wrapper(*args, **kw):
        with _ConnectionCtx():
            return func(*args, **kw)
    return _wrapper


@with_connection
def create(index_name, doc_type, doc_body, doc_id=None):
    global _db_ctx
    client = _db_ctx.client()
    result = client.create(index_name, doc_type, doc_body, doc_id)
    logging.info('<ES> info: create doc %s,index:%s,type:%s,id:%s' % (doc_body, index_name, doc_type, doc_id))
    return result


@with_connection
def index(index_name, doc_type, doc_body, doc_id=None):
    global _db_ctx
    client = _db_ctx.client()
    result = client.index(index_name, doc_type, doc_body, doc_id)
    logging.info('<ES> info: index doc %s,index:%s,type:%s,id:%s' % (doc_body, index_name, doc_type, doc_id))
    return result


@with_connection
def delete(index_name, doc_type, doc_id):
    global _db_ctx
    client = _db_ctx.client()
    result = client.delete(index_name, doc_type, doc_id)
    logging.info('<ES> info: delete index:%s,type:%s,id:%s' % (index_name, doc_type, doc_id))
    return result


@with_connection
def update()


@with_connection
def info():
    global _db_ctx
    client = _db_ctx.client()
    return client.info()


class DBError(Exception):
    pass


class _EngineError(Exception):
    pass


class _EsError(Exception):
    pass


class _Engine(object):
    def __init__(self, url, **kw):
        self.url = url
        self.kw = kw
        self.client = lambda :Elasticsearch(self.url, **self.kw)


class _Es(object):
    _count = 0

    def __init__(self):
        self.client = None
        self.actions = list()
        self.order = _Es._count
        _Es._count += 1

    def get_client(self):
        global engine
        if engine is not None:
            self.client = engine.client()
        else:
            raise _EngineError('get_client:_Engine Not create engine')

    def action(self, _index, _type, _id, _op_type='index', doc=None):
        _op_type_list = ('index', 'create', 'delete', 'update')
        if _op_type in _op_type_list:
            action = dict(_op_type=_op_type, _index=_index, _type=_type, _id=_id, doc=doc)
            self.actions.append(action)
        else:
            raise _EsError('action:_Es _op_type not in _op_type_list')

    def bulk(self):
        if self.client and (len(self.actions) > 0):
            helpers.bulk(self.client, self.actions)
        else:
            raise _EsError('commit:_Es have no client or actions = 0')

    def parallel_bulk(self,thread_count=4):
        if self.client and (len(self.actions) > 0):
            helpers.parallel_bulk(self.client, self.actions, thread_count)
        else:
            raise _EsError('commit:_Es have no client or actions = 0')

    def init_actions(self):
        self.actions = []


class _DbCtx(threading.local):
    def __init__(self):
        self.connection = None

    def is_init(self):
        return self.connection is not None

    def init(self):
        logging.info('open lazy connection...')
        self.connection = _Es()
        self.connection.get_client()

    def cleanup(self):
        self.connection = None

    def es(self):
        return self.connection

    def client(self):
        return self.connection.client

_db_ctx = _DbCtx()


class _ConnectionCtx(object):
    def __enter__(self):
        global _db_ctx
        self.should_cleanup = False
        if not _db_ctx.is_init():
            _db_ctx.init()
            self.should_cleanup = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        global _db_ctx
        if self.should_cleanup:
            _db_ctx.cleanup()


if __name__ == '__main__':

    create_engine_cfgfile()
    res = info()
    print('test info %s' % res)
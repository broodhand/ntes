# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 12:37:57 2016

@author: Zhao Cheng
"""
import logging;logging.basicConfig(level=logging.DEBUG)
import redis
import threading
import functools

connection = None
logstash_list = None


def _create_connection(host, port, db):
    global connection
    if connection is not None:
        raise DBError('connection is already initialized.')
    connection = _Connection(host, port, db)
    logging.info('Init redis connect <%s> ok.' % hex(id(connection)))


def create_connection(host='127.0.0.1', port='6379', db=0):
    _create_connection(host, port, db)


def create_connection_cfgfile(file='sync.cfg'):
    import configparser
    config = configparser.ConfigParser()
    with open(file, 'r') as cfgfile:
        config.read_file(cfgfile)
        host = config.get('REDIS', 'host')
        port = config.get('REDIS', 'port')
        db = config.get('REDIS', 'db')
    _create_connection(host, port, db)


def close_connection():
    global connection
    connection = None


def with_connection(func):
    @functools.wraps(func)
    def _wrapper(*args, **kw):
        with _connectionctx():
            return func(*args, **kw)
    return _wrapper


@with_connection
def rpush(listname, msg):
    global _db_ctx
    if isinstance(msg, str):
        _db_ctx.client.rpush(listname, msg)
    elif isinstance(msg, (tuple,list)):
        _db_ctx.client.rpush(listname, *msg)
    logging.debug('rpush to %s:\n %s' % (listname, msg))


def _logstash(listname):
    global logstash_list
    if logstash_list is not None:
        raise LogstashError('Already set up Logstash')
    else:
        logstash_list = listname


def setup_logstash(listname='logstash-list'):
    _logstash(listname)


def configfile_logstash(file='sync.cfg'):
    import configparser
    config = configparser.ConfigParser()
    with open(file, 'r') as cfgfile:
        config.read_file(cfgfile)
    listname = config.get('LOGSTASH', 'list')
    _logstash(listname)


def log(msg):
    global logstash_list
    if logstash_list is not None:
        rpush(logstash_list, msg)
    else:
        raise LogstashError('Need to setup Logstash')


class DBError(Exception):
    pass


class LogstashError(Exception):
    pass


class _Connection(object):
    def __init__(self, host, port, db):
        self.host = host
        self.port = port
        self.db = db
        self.pool = redis.ConnectionPool(host=self.host, port=self.port, db=self.db)
        self.client = redis.Redis(connection_pool=self.pool)


class _DbCtx(threading.local):
    def __init__(self):
        self.client = None

    def is_init(self):
        return self.client is not None

    def init(self):
        global connection
        logging.info('open redis client...')
        # logging.debug('redis server\'s info:\n %s' % connection.client.info())
        self.client = connection.client

    def cleanup(self):
        if self.is_init():
            self.client = None

    def client(self):
        return self.client

_db_ctx = _DbCtx()


class _connectionctx(object):
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



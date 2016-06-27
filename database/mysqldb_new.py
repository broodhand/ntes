#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2016/6/25 16:18

@project: Grandet
@version: 0.99
@file: mysqldb_new.py.py
@author: SPBG Co.,Ltd. ing / 北京正民惠浩投资管理有限公司 ing
@contact: ing@spbgcapital.com
@site: http://www.spbgcapital.net
"""
import time
import functools
import threading
import logging

logging.basicConfig(level=logging.INFO)

engine = None


def _profiling(start, sql=''):
    t = time.time() - start
    if t > 0.1:
        logging.warning('[PROFILING] [MYSQL] %s: %s' % (t, sql))
    else:
        logging.info('[PROFILING] [MYSQL] %s: %s' % (t, sql))


def create_engine(user, password, database, host='127.0.0.1', port=3306, **kw):
    import mysql.connector
    global engine
    if engine is not None:
        raise DBError('Engine is already initialized.')
    params = dict(user=user, password=password, database=database, host=host, port=port)
    defaults = dict(use_unicode=True, charset='utf8', collation='utf8_general_ci', autocommit=False)
    for (k, v) in defaults.items():
        params[k] = kw.pop(k, v)
    params.update(kw)
    params['buffered'] = True
    engine = _Engine(lambda: mysql.connector.connect(**params))
    logging.info('Init mysql engine <%s> ok.' % hex(id(engine)))


def use_cfgfile(func):
    @functools.wraps(func)
    def _wrapper(*args, **kw):


def connection():
    return _ConnectionCtx()


def with_connection(func):
    @functools.wraps(func)
    def _wrapper(*args, **kw):
        with _ConnectionCtx():
            return func(*args, **kw)
    return _wrapper


def transaction():
    return _TransactionCtx()


def with_transaction(func):
    """
       设计一个装饰器 替换with语法，让代码更优雅
       比如:
           @with_transaction
           def do_in_transaction():
       >>> @with_transaction
       ... def update_profile(id, name, rollback):
       ...     u = dict(id=id, name=name, email='%s@test.org' % name, passwd=name, last_modified=time.time())
       ...     insert('user', **u)
       ...     update('update user set passwd=? where id=?', name.upper(), id)
       ...     if rollback:
       ...         raise StandardError('will cause rollback...')
       >>> update_profile(8080, 'Julia', False)
       >>> select_one('select * from user where id=?', 8080).passwd
       'JULIA'
       >>> update_profile(9090, 'Robert', True)
       Traceback (most recent call last):
         ...
       StandardError: will cause rollback...
       """
    @functools.wraps(func)
    def _wrapper(*args, **kw):
        start = time.time()
        with _TransactionCtx():
            func(*args, **kw)
        _profiling(start)
    return _wrapper


@with_connection
def _select(sql, first, *args):
    global _db_ctx
    cursor = None
    names = None
    sql = sql.replace('?', '%s')
    logging.info('SQL: %s, ARGS: %s' % (sql, args))
    try:
        cursor = _db_ctx.connection.cursor()
        cursor.execute(sql, args)
        if cursor.description:
            names = [x[0] for x in cursor.description]
        if first:
            values = cursor.fetchone()
            if not values:
                return None
            return Dict(names, values)
        return [Dict(names, x) for x in cursor.fetchall()]
    finally:
        if cursor:
            cursor.close()


def select_one(sql, *args):
    """
    执行SQL 仅返回一个结果
    如果没有结果 返回None
    如果有1个结果，返回一个结果
    如果有多个结果，返回第一个结果
    >>> u1 = dict(id=100, name='Alice', email='alice@test.org', passwd='ABC-12345', last_modified=time.time())
    >>> u2 = dict(id=101, name='Sarah', email='sarah@test.org', passwd='ABC-12345', last_modified=time.time())
    >>> insert('user', **u1)
    1
    >>> insert('user', **u2)
    1
    >>> u = select_one('select * from user where id=?', 100)
    >>> u.name
    'Alice'
    >>> select_one('select * from user where email=?', 'abc@email.com')
    >>> u2 = select_one('select * from user where passwd=? order by email', 'ABC-12345')
    >>> u2.name
    'Alice'
     """
    return _select(sql, True, *args)


def select_int(sql, *args):
    """
    执行一个sql 返回一个数值，
    注意仅一个数值，如果返回多个数值将触发异常
    >>> u1 = dict(id=96900, name='Ada', email='ada@test.org', passwd='A-12345', last_modified=time.time())
    >>> u2 = dict(id=96901, name='Adam', email='adam@test.org', passwd='A-12345', last_modified=time.time())
    >>> insert('user', **u1)
    1
    >>> insert('user', **u2)
    1
    >>> select_int('select count(*) from user')
    5
    >>> select_int('select count(*) from user where email=?', 'ada@test.org')
    1
    >>> select_int('select count(*) from user where email=?', 'notexist@test.org')
    0
    >>> select_int('select id from user where email=?', 'ada@test.org')
    96900
    >>> select_int('select id, name from user where email=?', 'ada@test.org')
    Traceback (most recent call last):
        ...
    MultiColumnsError: Expect only one column.
    """
    d = _select(sql, True, *args)
    if len(d) != 1:
        raise MultiColumnsError('Expect only one column.')
    return tuple(d.values())[0]


def select(sql, *args):
    """
    执行sql 以列表形式返回结果
    >>> u1 = dict(id=200, name='Wall.E', email='wall.e@test.org', passwd='back-to-earth', last_modified=time.time())
    >>> u2 = dict(id=201, name='Eva', email='eva@test.org', passwd='back-to-earth', last_modified=time.time())
    >>> insert('user', **u1)
    1
    >>> insert('user', **u2)
    1
    >>> L = select('select * from user where id=?', 900900900)
    >>> L
    []
    >>> L = select('select * from user where id=?', 200)
    >>> L[0].email
    'wall.e@test.org'
    >>> L = select('select * from user where passwd=? order by id desc', 'back-to-earth')
    >>> L[0].name
    'Eva'
    >>> L[1].name
    'Wall.E'
    """
    return _select(sql, False, *args)


@with_connection
def _update(sql, *args):
    global _db_ctx
    cursor = None
    sql = sql.replace('?', '%s')
    logging.info('SQL: %s, ARGS: %s' % (sql, args))
    try:
        cursor = _db_ctx.connection.cursor()
        cursor.execute(sql, args)
        r = cursor.rowcount
        if _db_ctx.transactions == 0:
            logging.info('auto commit')
            _db_ctx.connection.commit()
        return r
    finally:
        if cursor:
            cursor.close()


def update(sql, *args):
    """
    执行update 语句，返回update的行数
    >>> u1 = dict(id=1000, name='Michael', email='michael@test.org', passwd='123456', last_modified=time.time())
    >>> insert('user', **u1)
    1
    >>> u2 = select_one('select * from user where id=?', 1000)
    >>> u2.email
    'michael@test.org'
    >>> u2.passwd
    '123456'
    >>> update('update user set email=?, passwd=? where id=?', 'michael@example.org', '654321', 1000)
    1
    >>> u3 = select_one('select * from user where id=?', 1000)
    >>> u3.email
    'michael@example.org'
    >>> u3.passwd
    '654321'
    >>> update('update user set passwd=? where id=?', '***', '123')
    0
    """
    return _update(sql, *args)


def insert(table, **kw):
    """
    执行insert语句
    >>> u1 = dict(id=2000, name='Bob', email='bob@test.org', passwd='bobobob', last_modified=time.time())
    >>> insert('user', **u1)
    1
    >>> u2 = select_one('select * from user where id=?', 2000)
    >>> u2.name
    'Bob'
    >>> insert('user', **u2)
    Traceback (most recent call last):
    ...
    mysql.connector.errors.IntegrityError: 1062 (23000): Duplicate entry '2000' for key 'PRIMARY'
    """
    cols, args = zip(*kw.items())
    sql = 'insert into `%s` (%s) values (%s)' % (table, ','.join(['`%s`' % col for col in cols]),
                                                 ','.join(['?' for i in range(len(cols))]))
    return _update(sql, *args)


class Dict(dict):
    def __init__(self, names=(), values=(), **kw):
        super(Dict, self).__init__(**kw)
        for k, v in zip(names, values):
            self[k] = v

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value


class DBError(Exception):
    pass


class MultiColumnsError(DBError):
    pass


class StandardError(Exception):
    pass


class _Engine(object):
    def __init__(self, connect):
        self._connect = connect

    def connect(self):
        return self._connect()


class _LazyConnection(object):
    def __init__(self):
        self.connection = None

    def cursor(self):
        if self.connection is None:
            _connection = engine.connect()
            logging.info('[CONNECTION] [OPEN] connection <%s>...' % hex(id(_connection)))
            self.connection = _connection
        return self.connection.cursor()

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()

    def cleanup(self):
        if self.connection:
            _connection = self.connection
            self.connection = None
            logging.info('[CONNECTION] [OPEN] connection <%s>...' % hex(id(_connection)))
            _connection.close()


class _DbCtx(threading.local):
    def __init__(self):
        self.connection = None
        self.transactions = 0

    def is_init(self):
        return self.connection is not None

    def init(self):
        logging.info('open lazy connection...')
        self.connection = _LazyConnection()
        self.transactions = 0

    def cleanup(self):
        self.connection.cleanup()
        self.connection = None

    def cursor(self):
        return self.connection.cursor()

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


class _TransactionCtx(object):
    def __enter__(self):
        global _db_ctx
        self.should_close_conn = False
        if not _db_ctx.is_init():
            _db_ctx.init()
            self.should_close_conn = True
        _db_ctx.transactions += 1
        logging.info('begin transaction...' if _db_ctx.transactions == 1 else 'join current transaction...')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        global _db_ctx
        _db_ctx.transactions -= 1
        try:
            if _db_ctx.transactions == 0:
                if exc_type is None:
                    self.commit()
                else:
                    self.rollback()
        finally:
            if self.should_close_conn:
                _db_ctx.cleanup()

    def commit(self):
        global _db_ctx
        logging.info('commit transaction...')
        try:
            _db_ctx.connection.commit()
            logging.info('commit ok.')
        except:
            logging.warning('commit failed.try rollback...')
            _db_ctx.connection.rollback()
            logging.warning('rollback ok.')
            raise

    def rollback(self):
        global _db_ctx
        logging.warning('rollback transaction...')
        _db_ctx.connection.rollback()
        logging.info('rollback ok.')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    create_engine('spbgcapital', '@Tnt7891011', 'spbgcapital', '192.168.1.160')
    update('drop table if exists user')
    update('create table user (id int primary key, name text, email text, passwd text, last_modified real)')
    import doctest
    doctest.testmod()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 12:37:57 2016
@author: Zhao Cheng
__version__ = '0.0.1'
"""
import time
import functools
import threading
import logging

logging.basicConfig(level=logging.WARNING)


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
    >>> close_engine()
    >>> create_engine_cfgfile()
    >>> update('drop table if exists user')
    0
    >>> update('create table user (id int primary key, name text, email text, passwd text, last_modified real)')
    0
    >>> u1 = dict(id=100, name='Alice', email=tmp_test, passwd='ABC-12345', last_modified=time.time())
    >>> u2 = dict(id=101, name='Sarah', email=tmp_test, passwd='ABC-12345', last_modified=time.time())
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
    >>> close_engine()
    >>> create_engine_cfgfile()
    >>> update('drop table if exists user')
    0
    >>> update('create table user (id int primary key, name text, email text, passwd text, last_modified real)')
    0
    >>> u1 = dict(id=96900, name='Ada', email='ada@test.org', passwd='A-12345', last_modified=time.time())
    >>> u2 = dict(id=96901, name='Adam', email='adam@test.org', passwd='A-12345', last_modified=time.time())
    >>> insert('user', **u1)
    1
    >>> insert('user', **u2)
    1
    >>> select_int('select count(*) from user')
    2
    >>> select_int('select count(*) from user where email=?', 'ada@test.org')
    1
    >>> select_int('select count(*) from user where email=?', 'notexist@test.org')
    0
    >>> select_int('select id from user where email=?', 'ada@test.org')
    96900
    >>> select_int('select id, name from user where email=?', 'ada@test.org') #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        ...
    sync.MultiColumnsError: Expect only one column.
    """
    d = _select(sql, True, *args)
    if len(d) != 1:
        raise MultiColumnsError('Expect only one column.')
    return tuple(d.values())[0]


def select(sql, *args):
    """
    执行sql 以列表形式返回结果
    >>> close_engine()
    >>> create_engine_cfgfile()
    >>> update('drop table if exists user')
    0
    >>> update('create table user (id int primary key, name text, email text, passwd text, last_modified real)')
    0
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
    >>> close_engine()
    >>> create_engine_cfgfile()
    >>> update('drop table if exists user')
    0
    >>> update('create table user (id int primary key, name text, email text, passwd text, last_modified real)')
    0
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
    >>> close_engine()
    >>> create_engine_cfgfile()
    >>> update('drop table if exists user')
    0
    >>> update('create table user (id int primary key, name text, email text, passwd text, last_modified real)')
    0
    >>> u1 = dict(id=2000, name='Bob', email=tmp_test, passwd='bobobob', last_modified=time.time())
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



if __name__ == '__main__':
    import doctest
    doctest.testmod()

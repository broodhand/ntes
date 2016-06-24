#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2016/6/23 23:12

@project: Grandet
@version: 0.99
@file: mysqldb.py
@author: SPBG Co.,Ltd. ing / 北京正民惠浩投资管理有限公司 ing
@contact: ing@spbgcapital.com
@site: http://www.spbgcapital.net
"""
import mysql.connector
import configparser
import logging
logging.basicConfig(level=logging.INFO)
__pool = None


def create_pool(file='mysqldb.cfg'):
        global __pool
        config = configparser.ConfigParser()
        with open(file, 'r') as cfgfile:
            config.read_file(cfgfile)
            host = config.get('MYSQL', 'host')
            user = config.get('MYSQL', 'user')
            password = config.get('MYSQL', 'password')
            database = config.get('MYSQL', 'database')
            constr = {'host': host, 'user': user, 'password': password, 'database': database}
            __pool = mysql.connector.connect(**constr)


def select(sql, args, size=None):
    global __pool
    cur = __pool.cursor()
    cur.execute(sql.replace('?', '%s'), args or ())
    if size:
        rs = cur.fetchmany(size)
    else:
        rs = cur.fetchall()
    cur.close
    return rs


def execute(sql, args):
    global __pool
    try:
        cur = __pool.cursor()
        cur.execute(sql.replace('?', '%s'), args)
        affected = cur.rowcount
        cur.close()
    except BaseException as e:
            raise
    return affected

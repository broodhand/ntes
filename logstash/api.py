# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 12:37:57 2016
@author: Zhao Cheng
__version__ = '0.1.0'
Create logstash API to use the logstash which pass the data from redis to elasticsearch.
"""
import logging; logging.basicConfig(level=logging.DEBUG)
import redis
import redisDB
import json
from . import config

rediscfg = config.logstash['redisAPI_config']  # Get config from config.py
loglist = config.logstash['logstash_listname']  # Get redis list key name for logstash


def _vaild_dict(dictmsg):
    """
    Check if dict input is fit for logstash.
    :param dictmsg: Only can input dict
    :return: True(Success)
    """
    for value in dictmsg.values():
        if not isinstance(value, (dict, str, float, int)):
            raise ValueError('Dict values Must be dict, str,float and int')
        if isinstance(value, dict):
            _vaild_dict(value)
    return True


def _vaild_list(listmsg):
    """
    Check if list input is fit for logstash.
    :param listmsg: Only can input list
    :return: True(Success)
    """
    for item in listmsg:
        _vaild_dict(item)
    return True


@redisDB.with_connection(**rediscfg)
def _log(msg, client=None, keyname=loglist):
    """
    Push message to the redis list which logstash used.
    Using redisDB.with_connection to Auto connect redis and pass client to _log()
    :param msg: json string or json string's list
    :return: Result of rpush(the item number in the list)
    """
    return client.rpush(keyname, msg)


def log(msg):
    """
    Verify that data is fit for logstash.
    Auto convert python object to json string or json string's list
    :param msg: dict, list, tuple object which push to logstash
    :return: Result of rpush(the item number in the list)
    """
    if isinstance(msg, dict):
        if _vaild_dict(msg):
            msgjson = json.dumps(msg)
            return _log(msgjson)
    if isinstance(msg, (list, tuple)):
        if _vaild_list(msg):
            msgjson = tuple(map(json.dumps, msg))
            return _log(msgjson)
    else:
        raise ValueError('log(msg) msg must be dict,list and tuple')


def _push(msg, client, keyname=loglist):
    """
    Push message to the redis list which the logstash used.
    Not to auto connect the redis.
    Can use 'with redisDB.redis_connection() as :' to push many datas,but connect the redis once.
    :param msg: json string or json string's list
    :return: Result of rpush(the item number in the list)
    """
    if not isinstance(client, redis.StrictRedis):
        raise redis.RedisError('Must use "with redisDB.connection(rediscfg)"')
    return client.rpush(keyname, msg)


def push(msg, client):
    """
    Verify that data is fit for logstash.Not to auto connect redis.
    Auto convert python object to json string or json string's list
    :param client: redis.StrictRedis or redis.Redis instance
    :param msg: dict, list, tuple object which push to logstash
    :return: Result of rpush(the item number in the list)
    """
    if isinstance(msg, dict):
        if _vaild_dict(msg):
            msgjson = json.dumps(msg)
            return _push(msgjson, client)
    if isinstance(msg, (list, tuple)):
        if _vaild_list(msg):
            msgjson = tuple(map(json.dumps, msg))
            return _push(msgjson, client)
    else:
        raise ValueError('log(msg) msg must be dict,list and tuple')
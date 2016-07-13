# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 12:37:57 2016
@author: Zhao Cheng

Create logstash API to use the logstash which pass the data from redis to elasticsearch.
"""
import logging; logging.basicConfig(level=logging.DEBUG)
import redisAPI
import json
from . import config

_rediscfg = config.rediscfg  # Get config from config.py
_loglist = config.logstashlist  # Get redis list key name for logstash


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


@redisAPI.with_redis(**_rediscfg)
def _log(msg):
    """
    Push message to the redis list which logstash used.
    Using redisAPI.with_redis to Auto connect redis.
    :param msg: json string or json string's list
    :return: True(Success)
    """
    global _loglist
    return redisAPI.rpush(_loglist, msg)


def log(msg):
    """
    Verify that data is fit for logstash.
    Auto convert python object to json string or json string's list
    :param msg: dict, list, tuple object which push to logstash
    :return: True(Success)
    """
    if isinstance(msg, dict):
        if _vaild_dict(msg):
            msgjson = json.dumps(msg)
            return _log(msgjson)
    if isinstance(msg, (list, tuple)):
        if _vaild_list(msg):
            msgjson = tuple(map(json.dumps, msg))
            return _log(msgjson)


def _push(msg):
    """
    Push message to the redis list which the logstash used.
    Not to auto connect the redis.
    Can use 'with redisAPI.redis_connection():' to push many datas,but connect the redis once.
    :param msg: json string or json string's list
    :return: True(Success)
    """
    global _loglist
    return redisAPI.rpush(_loglist, msg)


def push(msg):
    """
    Verify that data is fit for logstash.Not to auto connect redis.
    Auto convert python object to json string or json string's list
    :param msg: dict, list, tuple object which push to logstash
    :return: True(Success)
    """
    if isinstance(msg, dict):
        if _vaild_dict(msg):
            msgjson = json.dumps(msg)
            return _push(msgjson)
    if isinstance(msg, (list, tuple)):
        if _vaild_list(msg):
            msgjson = tuple(map(json.dumps, msg))
            return _push(msgjson)



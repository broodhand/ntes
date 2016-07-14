# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 12:37:57 2016
@author: Zhao Cheng

Create Redis APIs
"""
import logging; logging.basicConfig(level=logging.DEBUG)
import functools
from . import client


def _check_client(func):
    """
    for using "@check_client"
    """
    @functools.wraps(func)
    def _wrapper(*args, **kw):
        if client.have_client():
            kw['redis_client'] = client.get_client()
            return func(*args, **kw)
        else:
            raise client.RedisError('Need to connect redis')
    return _wrapper


@_check_client
def rpush(listname, msg, redis_client=None):
    """
    To rpush msg to the redis list
    :param redis_client: redis redis from module redis method get_client.
    :param listname:redis list name
    :param msg: rpush message to redis
    :return: Result of rpush(the item number in the list)
    """
    if isinstance(msg, str):
        return redis_client.rpush(listname, msg)
    elif isinstance(msg, (tuple, list)):
        return redis_client.rpush(listname, *msg)
    else:
        raise ValueError('Must be str or list')


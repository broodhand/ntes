# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 12:37:57 2016

@author: Zhao Cheng
"""
import logging; logging.basicConfig(level=logging.DEBUG)
from .client import with_client


@with_client
def rpush(listname, msg):
    from .client import _client
    if isinstance(msg, str):
        _client.redis.rpush(listname, msg)
    elif isinstance(msg, (tuple, list)):
        _client.redis.rpush(listname, *msg)
    else:
        raise ValueError('Must be str or list')
    logging.debug('rpush to %s:\n %s' % (listname, msg))


# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 12:37:57 2016
@author: Zhao Cheng

Create Redis API to use the redis client
"""
import logging; logging.basicConfig(level=logging.DEBUG)
from .client import with_client


@with_client
def rpush(listname, msg):
    """
    To rpush msg to the redis list
    :param listname:redis list name
    :param msg: the message rpush to redis
    :return: True Success
    :return: None Fail
    """
    from .client import _client

    r = _client.redis

    if isinstance(msg, str):
        r.rpush(listname, msg)
    elif isinstance(msg, (tuple, list)):
        r.rpush(listname, *msg)
    else:
        raise ValueError('Must be str or list')
    logging.debug('rpush to %s:\n %s' % (listname, msg))
    return True

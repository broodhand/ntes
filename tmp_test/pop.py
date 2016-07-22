# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 11:02:14 2016

@author:Zhao Cheng
"""

import db
data = []


def callback(dictdata):
    if len(data) < 10:
        data.append(dictdata)
    else:
        while len(data) > 0:
            print(data.pop())
    return None

redis = db.RedisDB()
redis.pop_stream(callback_func=callback)

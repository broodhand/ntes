# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 11:02:14 2016

@author:Zhao Cheng
"""

import database
data = []


def callback(dictdata):
    if len(data) < 10:
        data.append(dictdata)
    else:
        while len(data) > 0:
            print(data.pop())
    return None

redis = database.RedisDB()
redis.popdata(callback_func=callback)

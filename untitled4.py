# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 12:37:57 2016

@author: Administrator
"""

from ntes import ntesdata
import redis,json

r = redis.StrictRedis(host='spbgcapital.f3322.net',port=6379,db=0)

def callback(input):
    print(json.dumps(input))
  #  r.rpush('ntes',json.dumps(input)
    




data =ntesdata('204001').get_sn(callback)


'''
while True:
    data = ntesdata('150201').get()
    print(r.rpush('test',data))
    time.sleep(0.05)
'''
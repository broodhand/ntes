# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 11:19:05 2016

@author: Administrator
"""
import redis

r = redis.StrictRedis(host='spbgcapital.f3322.net',port=6379,db=0)


while True:
    if r.llen('ntes')>0:
        print(r.lpop('ntes'))
        print(r.llen('ntes'))
        
    

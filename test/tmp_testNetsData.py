# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 13:07:18 2016

@author: Administrator
"""

from urllib import request
import json,re,time


time1=''
update=''
with request.urlopen('http://api.money.126.net/data/feed/1160220,money.api') as f:
        data = f.read()
        myjson = re.search(r'\(.*\)',data.decode('utf-8'))
        myjson1 = myjson.group(0)
        myjson3 = myjson1[1:-1]
        decode1 = json.loads(myjson3)
        decode2 = decode1
while True :
    with request.urlopen('http://api.money.126.net/data/feed/1160220,money.api') as f:
        data = f.read()
        myjson = re.search(r'\(.*\)',data.decode('utf-8'))
        myjson1 = myjson.group(0)
        myjson3 = myjson1[1:-1]
        decode1 = json.loads(myjson3)
      #  del decode1['1160220'][]
        time1 = decode1['1160220']['time']
        update1 = decode1['1160220']['update']
        del decode1['1160220']['time']
        del decode1['1160220']['update']       
        if decode2 != decode1:
            print(decode1['1160220']['name'],time1,update1,decode1['1160220']['price'])            
            for (d,x) in decode1['1160220'].items():
                if x != decode2['1160220'][d]:
                    print(d,x)
                    print(d,decode2['1160220'][d])
            decode2 = decode1  
        time.sleep(1)
#data = []
#data['code'] = decode1   
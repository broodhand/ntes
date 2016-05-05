# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 11:25:37 2016

@author: Zhao Cheng
"""
from urllib import request
import json

#获取网易数据的类
class ntesdata(object):
    
    def __init__(self,code):
        self.code = code
        
    def get(self):
        fronturl = 'http://api.money.126.net/data/feed/'
        backurl = ',money.api'
        L = [fronturl+str(x)+self.code+backurl for x in range(10)]     
        for url in L:
            with request.urlopen(url) as f:
                data = f.read()
            data_proc = data.decode('utf-8')[21:-2]
            if data_proc != '{ }':
                return(list(json.loads(data_proc).values())[0])

    def __procdata(self,data):
        if data != None:        
            dict_data = data.copy()
            ntes_time = dict_data.pop('time')
            ntes_update = dict_data.pop('update')
            return {'time':ntes_time,'update':ntes_update,'data':dict_data}
        return None
    
    def get_sn(self,func):
        data_init = self.__procdata(self.get())
        if data_init != None:
            func(data_init)
        while True:
            data_new = self.__procdata(self.get())
            if data_new != None :
                if data_new['data'] != data_init['data']:
                    func(data_new)
                    data_init = data_new
                    
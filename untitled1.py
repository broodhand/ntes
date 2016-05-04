# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 11:25:37 2016

@author: Zhao Cheng
"""
from urllib import request

class ntesdata(object):
    
    def __init__(self,code):
        self.code = code
        
    def get(self):
        fronturl = 'http://api.money.126.net/data/feed/'
        backurl = ',money.api'
        L = [fronturl+str(x)+self.code+backurl for x in range(10)]
        L1 = []        
        for url in L:
            with request.urlopen(url) as f:
                data = f.read()
                data_proc = data.decode('utf-8')[21:-2]
                if data_proc != '{ }':
                    L1.append(data_proc)
        return L1
        

# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 10:57:52 2016

@author: Administrator
"""
from old_ntes import ntesdata

import json,time


data = ntesdata('150201').get()

    


'''    
decode1 = json.loads(data.get('204001'))
decode2 = decode1
while True :
        decode1 = json.loads(ntesdata.get('204001'))
        print(decode1.keys()) 
'''


'''
     #  del decode1['1160220'][]
        time1 = decode1['']['time']
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
'''
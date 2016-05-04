# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 14:24:10 2016

@author: Administrator
"""

from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch import helpers

es=Elasticsearch('spbgcapital.f3322.net:9200')
actions=[]
for j in range(500):
    action={"_index":"test_index",
            "_type":"test_type",
            "_id":j,
            "_source":{
            "any":"data"+str(j),
            "timestamp":datetime.now()            
                }
            }
    actions.append(action)
    
if len(actions)>0:
    helpers.bulk(es,actions)
           
            
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 14:24:10 2016

@author: Zhao Cheng
"""

from elasticsearch import Elasticsearch
from elasticsearch import helpers
import configparser


class EsDB(object):
    def __init__(self, esindex, estype, esid=None, escfg='elasticsearchdb.cfg'):
        self.esindex = esindex
        self.estype = estype
        self.escfg = escfg
        self.esid = esid
        config = configparser.ConfigParser()
        with open(self.escfg, 'r') as cfgfile:
            config.read_file(cfgfile)
            self.cfghost = config.get('ELASTICSEARCH', 'host')
            self.cfgport = config.get('ELASTICSEARCH', 'port')
        self.server = self.cfghost + ':' + self.cfgport

    def connect(self):
        return Elasticsearch(self.server)

    def put(self, esdatas):
        es = self.connect()
        actions = []
        for data in esdatas:
            if self.esid is not None:
                action = {"_index": self.esindex,
                          "_type": self.estype,
                          "_id": self.esid,
                          "_source": data
                          }
            else:
                action = {"_index": self.esindex,
                          "_type": self.estype,
                          "_source": data
                          }
            actions.append(action)
        if len(actions) > 0:
            helpers.bulk(es, actions)

actions_cache = []


def callback_es(esdata):
    if isinstance(esdata, dict):
        esindex = esdata['sources']
        estype = esdata['type']
        action = {"_index": esindex,
                  "_type": estype,
                  "_source": esdata
                  }
    actions_cache.append(action)

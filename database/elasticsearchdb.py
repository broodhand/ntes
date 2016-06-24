# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 14:24:10 2016

@author: Zhao Cheng
"""

from elasticsearch import Elasticsearch
from elasticsearch import helpers
import configparser
__action = list()

class EsDB(object):
    def __init__(self, escfg='elasticsearchdb.cfg'):
        config = configparser.ConfigParser()
        with open(escfg, 'r') as cfgfile:
            config.read_file(cfgfile)
            self.cfghost = config.get('ELASTICSEARCH', 'host')
            self.cfgport = config.get('ELASTICSEARCH', 'port')
        self.server = self.cfghost + ':' + self.cfgport

    def connect(self):
        return Elasticsearch(self.server)

    def put(self, esindex, estype, esid, esdatas):
        es = self.connect()
        global  __action
            if self.esid is not None:
                action = {"_index": esindex,
                          "_type": estype,
                          "_id": esid,
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

# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 11:02:14 2016

@author:Zhao Cheng
"""

# Get the stock data from api.money.126.net

from urllib import request
import json
import time
import types


# Get the data which from the nets stock api


class TickData(object):
    # Get the stocks' code for the class's initial property
    def __init__(self, code):
        self.code = code

    # Get the json data from nets api
    @property
    def value(self):
        fronturl = 'http://api.money.126.net/data/feed/'
        backurl = ',money.api'
        urllist = [fronturl + str(x) + self.code + backurl for x in range(10)]
        for url in urllist:
            with request.urlopen(url) as f:
                data = f.read()
            data_proc = data.decode('utf-8')[21:-2]
            if data_proc != '{ }':
                dictdata = list(json.loads(data_proc).values())[0]
                if isinstance(dictdata,dict):
                    dictdata['source'] = 'nets'
                return dictdata

    # Get the value from the nets api.This is a generator.
    # The 'interval' which is a parameter is control the interval between twice
    # getting data.
    def value_generator(self, interval=3):
        while True:
            yield self.value
            time.sleep(interval)

    # Get the value form the nets api.This is a data stream.
    # You can get data from callback function.
    def value_stream(self, interval=3, callback_func=lambda x: print(x)):
        # Get the data without time and update
        initvalue = self.value
        initdata = None
        newdata = None

        def __proc(data_dict):
            if isinstance(data_dict, dict):
                data = data_dict.copy()
                if ('time' in data) and ('update' in data):
                    return {'time': data.pop('time'), 'update': data.pop('update'), 'data': data}
            return None

        if isinstance(callback_func, types.FunctionType):
            if initvalue:
                callback_func(initvalue)
            for newvalue in self.value_generator(interval):
                if isinstance(initvalue, dict):
                    initdata = __proc(initvalue).get('data')
                if isinstance(newvalue, dict):
                    newdata = __proc(newvalue).get('data')
                if newvalue and (newdata != initdata):
                    callback_func(newvalue)
                    initvalue = newvalue
# End


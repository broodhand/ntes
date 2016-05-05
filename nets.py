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


# Get the data which from the NTES stock api


class NtesTickData(object):
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
                return list(json.loads(data_proc).values())[0]

    # Get the value from the nets api.This is a generator.
    # The 'interval' which is a parameter is control the interval between twice
    # getting data.
    def value_generator(self, interval=3):
        while True:
            yield self.value
            time.sleep(interval)

    # Get the value form the ntes api.This is a data stream.
    # You can get data from callback function.
    def value_stream(self, interval=3, callback_func=lambda x: print(x)):
        # Get the data without time and update
        def __proc(data_dict):
            if isinstance(data_dict, dict):
                data = data_dict.copy()
                if ('time' in data) and ('update' in data):
                    return {'time': data.pop('time'), 'update': data.pop('update'), 'data': data}
            return None

        v_init = self.value
        data_init = None
        data_new = None

        if isinstance(callback_func, types.FunctionType):
            if v_init:
                callback_func(v_init)
            for v_new in self.value_generator(interval):
                if isinstance(v_init, dict):
                    data_init = __proc(v_init).get('data')
                if isinstance(v_new, dict):
                    data_new = __proc(v_new).get('data')
                if v_new and (data_new != data_init):
                    callback_func(v_new)
                    v_init = v_new
# End

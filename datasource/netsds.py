# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 11:02:14 2016

@author:Zhao Cheng
"""

# Get the stock data from api.money.126.net
from datetime import datetime
from datastructure import Cache
import json
import time
import types
import logging
logging.basicConfig(level=logging.INFO)
# Get the data which from the nets stock api

# Get the nets code
def getncode(code):
    from urllib import request

    if isinstance(code, int):
        code = str(code)

    if isinstance(code, str):
        fronturl = 'http://api.money.126.net/data/feed/'
        backurl = ',money.api'
        ncodelist = [str(x) + code for x in range(10)]

        for ncode in ncodelist:
            url = fronturl + ncode + backurl

            with request.urlopen(url) as f:
                data = f.read()

            data_proc = data.decode('utf-8')[21:-2]

            if data_proc != '{ }':
                return ncode


def getncode1(code):
    from urllib import request

    fronturl = 'http://api.money.126.net/data/feed/'
    backurl = ',money.api'
    codes = list()
    if isinstance(code,int)

    if isinstance(code, (str, int)):
        codes.append(code)
        codes = tuple(codes)
    elif isinstance(code, (list, tuple)):
        codes = tuple(code)
    logging.info(codes)

       # ncodelist = [str(x) + code for x in range(10)]
   # codestr = ','.join(ncodelist)
  #  url = fronturl + codestr + backurl
  #  with request.urlopen(url) as f:
    #    return f.read()


def getncodes(codes):
    ncodes = list()
    if isinstance(codes, (int, str)):
        ncodes.append(getncode(codes))
    elif isinstance(codes, (list, tuple)):
        for code in codes:
            if isinstance(code, (int, str)):
                ncodes.append(getncode(code))
    return tuple(ncodes)


class TNets(object):
    # Get the stocks' code for the class's initial property
    def __init__(self, code):
        if isinstance(code, int):
            self.code = str(code)
        else:
            self.code = code
        self.ncodes = getncode(self.code)

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
                if isinstance(dictdata, dict):
                    dictdata['source'] = 'nets'
                    dictdata['type'] = 'tick'
                return dictdata

    # Get the value from the nets api.This is a generator.
    # The 'interval' which is a parameter is control the interval between twice
    # getting data.
    def value_generator(self, interval=3):
        while 1:
            yield self.value
            time.sleep(interval)

    # Get the value form the nets api.This is a data stream.
    # You can get data from callback function.
    def value_stream(self, callback_func=lambda x: print(x), interval=3):
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

    # The stream class with the cache function
    def value_cachestream(self, callback_func=lambda x: print(x), interval=3, cachenum=500, cacheseconds=60):
        # Get the data without time and update
        def __proc(data_dict):
            if isinstance(data_dict, dict):
                data = data_dict.copy()
                if ('time' in data) and ('update' in data):
                    return {'time': data.pop('time'), 'update': data.pop('update'), 'data': data}
            return None

        initvalue = self.value
        initdata = None
        newdata = None
        cache = Cache(num=cachenum, seconds=cacheseconds)
        proctime = datetime.now()
        if isinstance(callback_func, types.FunctionType):

            if initvalue:
                cache.push(initvalue)
                tmpdata = cache.pop()

                if tmpdata:
                    callback_func(tmpdata)

                proctime = datetime.now()

            for newvalue in self.value_generator(interval):
                if isinstance(initvalue, dict):
                    initdata = __proc(initvalue).get('data')

                if isinstance(newvalue, dict):
                    newdata = __proc(newvalue).get('data')

                if newvalue and (newdata != initdata):
                    cache.push(newvalue)
                    tmpdata = cache.pop()

                    if tmpdata:
                        callback_func(tmpdata)

                    proctime = datetime.now()
                    initvalue = newvalue

                elif (datetime.now()-proctime).seconds >= cacheseconds and cache.proc:
                    tmpdata = cache.pop()

                    if tmpdata:
                        callback_func(tmpdata)
                        proctime = datetime.now()

    def value_cachestream2(self, callback_func=lambda x: print(x), interval=3, cachenum=500, cacheseconds=60):
        # Get the data without time and update
        from multiprocessing import Process
        from multiprocessing import Queue
        import os
        cache = Cache(num=cachenum, seconds=cacheseconds)
        callback_cache = cache.push
        q = Queue()
        pid = os.fork()
        if pid == 0:
            self.value_stream(callback_cache)
        else:
            for data in cache.stream(interval):
                callback_func(data)


# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 11:02:14 2016

@author:Zhao Cheng
"""

# 通过api获取网易数据
from datetime import datetime
from datastructure import Cache
from urllib import request
import time
import types
import logging
logging.basicConfig(level=logging.INFO)


# 通过网易代码异步获取网易api数据，最大限制1000数据
async def __asyncgetnvalue(sessions, results, *codes):
    import aiohttp
    fronturl = 'http://api.money.126.net/data/feed/'
    backurl = ',money.api'
    codelist = list()

    logging.info('input nets api data number: %s' % len(codes))

    if len(codes) > 1010:
        raise ValueError('Too many code input: %s' % len(codes))

    for code in codes:
        codelist.append(str(code))

    url = fronturl + ','.join(codelist) + backurl
    with aiohttp.Timeout(10):
        async with sessions.get(url) as response:
            results.append(await response.text())


# 通过网易代码获取网易api数据
def getnvalue(*codes):
    import asyncio
    import aiohttp
    import json
    lcodes = list()
    task = list()
    result = list()
    dictdata = dict()
    for i in range(0, len(codes), 1000):
        lcodes.append(codes[i:i + 1000])

    loop = asyncio.get_event_loop()

    with aiohttp.ClientSession(loop=loop) as session:
        for ncodes in lcodes:
            task.append(__asyncgetnvalue(session, result, *ncodes))
        loop.run_until_complete(asyncio.wait(task))
    for item in result:
        logging.info('get the data number: %s' % len(json.loads(item[21:-2])))
        dictdata.update(json.loads(item[21:-2]))
    return dictdata


# 通过标准代码获取网易代码
def getncode(*codes):
    listcode = list()
    logging.info('input getnvalue data number: %s' % len(codes))

    for code in codes:
        listcode = listcode + [str(x) + str(code) for x in range(10)]

    dictdata = getnvalue(*listcode)
    dictcode = dict()
    for key in dictdata:
        dictcode[key[1:]] = key

    return dictcode


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


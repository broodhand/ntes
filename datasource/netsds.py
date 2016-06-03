# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 11:02:14 2016

@author:Zhao Cheng
"""

# 通过api获取网易证券数据
from datetime import datetime
from datastructure import Cache
from urllib import request
import types
import asyncio
import aiohttp
import json
import time
import logging
logging.basicConfig(level=logging.INFO)


# 生成所有可能代码,digit为代码位数,outtype为输出数据格式可以为list,tuple,generator
def __codegenerator(digit, outtype='list'):
    if isinstance(digit, int):
        if outtype == 'list':
            return [str(x).zfill(digit) for x in range(10 ** digit)]
        if outtype == 'tuple':
            return tuple([str(x).zfill(digit) for x in range(10 ** digit)])
        if outtype == 'generator':
            return (str(x).zfill(digit) for x in range(10 ** digit))


# 对list进行切片
def __codecut(code, slices=1000):
    if isinstance(code, (list, tuple)):
        lcodes = list()
        for i in range(0, len(code), slices):
            lcodes.append(code[i:i + slices])
        return lcodes


# 通过网易代码异步获取网易api数据，最大限制1000数据
async def __asyncgetnvalue(sessions, future, *codes):
    fronturl = 'http://api.money.126.net/data/feed/'
    backurl = ',money.api'
    codelist = list()

    logging.info('__asyncgetnvalue:Input data number %s' % len(codes))

    if len(codes) > 1010:
        raise ValueError('Too many code input: %s' % len(codes))

    for code in codes:
        codelist.append(str(code))

    url = fronturl + ','.join(codelist) + backurl
    with aiohttp.Timeout(10):
        async with sessions.get(url) as response:
            future.set_result(await response.text())


# 通过网易代码并发获取网易api数据
def __getnvalue(*codes, slices=1000):
    task = list()
    dictdata = dict()
    futurelist = list()
    loop = asyncio.get_event_loop()
    lcodes = __codecut(codes, slices=slices)

    with aiohttp.ClientSession(loop=loop) as session:
        for index, ncodes in enumerate(lcodes):
            futurelist.append(asyncio.Future())
            task.append(asyncio.ensure_future(__asyncgetnvalue(session, futurelist[index], *ncodes)))
        loop.run_until_complete(asyncio.wait(task))

    for future in futurelist:
        item = future.result()
        logging.info('getnvalue: Getting the data number %s' % len(json.loads(item[21:-2])))
        dictdata.update(json.loads(item[21:-2]))

    logging.info('getnvalue: Total received data number %s' % len(dictdata))
    return dictdata


# 不限数量网易代码并发获取网易api数据,不对错误穷举处理,curnum 为最大并发数, slicesnum 为每协程切片数量 ,interval 为并发间隔
def getnvalue(*codes, curnum=400, slicesnum=1000, interval=32):
    import time
    if slicesnum > 1000:
        raise ValueError('The slicesnum must less than 1000: %s' % slicesnum)
    result = dict()
    errorlist = list()
    listcode = __codecut(codes, slices=(slicesnum * curnum))

    for index, codes in enumerate(listcode):
        try:
            r = __getnvalue(*codes)
        except Exception as e:
            logging.info(e)
            errorlist += codes
        else:
            if isinstance(r, dict):
                result.update(r)
                logging.info('receive data: %s' % r)
                logging.info('running %s / %s ,get %s data' % (index + 1, len(listcode), len(result)))
            else:
                errorlist += codes
        if not (index + 1) == len(listcode):
            time.sleep(interval)

    return result, errorlist


# 通过网易代码并发获取有效网易api数据,对错误穷举处理,curnum 为最大并发数,interval 为并发间隔
def getvalue(*codes, curnum=400, interval=32):
    import time
    result = dict()
    r_init = getnvalue(*codes, curnum=curnum, interval=interval)
    result.update(r_init[0])
    slicesnum = 100
    while slicesnum > 0 and len(r_init[1]) > 0:
        r_next = getnvalue(*r_init[1], curnum=curnum, slicesnum=slicesnum, interval=interval)
        if len(r_next[0]) > 0:
            result.update(r_next[0])
            r_init = r_next
        elif not len(r_next[1]) == len(r_init[1]):
            r_init = r_next
        else:
            slicesnum //= 10
        time.sleep(interval)
    return result, r_init[1]


# 获取有效网易代码
def getcode(*codes, curnum=10, interval=60):
    logging.info('getncode: Input data number %s' % len(codes))
    data = getvalue(*codes, curnum=curnum, interval=interval)
    dictdata = data[0]
    listerror = data[1]
    dictcode = dict()
    for (k, v) in dictdata.items():
        if isinstance(v, dict):
            if v.get('symbol'):
                dictcode[v.get('symbol')] = k
            else:
                listerror.append(k)
    return dictcode, listerror


# 通过标准六位代码获取有效网易代码
def getncode(*codes):
    listcode = list()
    logging.info('getncode: Input data number %s' % len(codes))

    for code in codes:
        listcode += [str(x) + str(code) for x in range(10)]

    dictdata = getnvalue(*listcode)
    dictcode = dict()
    for key in dictdata:
        dictcode[key[1:]] = key

    return dictcode


# 通过标准六位代码切片list获得有效网易代码及错误解析代码
def getcode_slices(codelist):
    import time
    result = dict()
    errorlist = list()
    for index, codes in enumerate(codelist):
        try:
            r = getncode(*codes)
        except Exception as e:
            logging.info(e)
            errorlist.append(codes)
        else:
            if isinstance(r, dict):
                result.update(r)
            else:
                errorlist.append(codes)
        logging.info('receive data: %s' % r)
        logging.info('running %s / %s ,get %s data' % (index+1, len(codelist), len(result)))
        time.sleep(10)
    return result, errorlist


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


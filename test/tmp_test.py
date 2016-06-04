# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 11:02:14 2016

@author:Zhao Cheng
"""
# 通过api获取网易证券数据


import logging
import asyncio
import aiohttp
import json

logging.basicConfig(level=logging.INFO)


def tmp_test():
    raise ValueError
    print('abc')


# 对list,tuple进行切片
def cut_list(code, slices=1000):
    if isinstance(code, (list, tuple)):
        lcodes = list()
        for i in range(0, len(code), slices):
            lcodes.append(code[i:i + slices])
        return lcodes
    else:
        raise TypeError('Input data must be list or tuple object')


# 开启一个协程异步获取网易api数据，最大限制1000数据
async def __asyncgetnvalue(sessions, future, dictdata, index, num, *codes, timeout=30):
    if len(codes) > 1010:
        raise ValueError('Too many code input: %s' % len(codes))

    fronturl = 'http://api.money.126.net/data/feed/'
    backurl = ',money.api'
    codelist = list()

    def got_result(fut):
        data = fut.result()
        dictdata.update(json.loads(data[21:-2]))
        num[0] -= 1
        num[1] -= 1
        logging.info('%s End,remain %s/%s' % (index, num[1], num[2]))

    logging.info('__asyncgetnvalue:Input data number %s' % len(codes))

    if len(codes) > 1010:
        raise ValueError('Too many code input: %s' % len(codes))

    for code in codes:
        codelist.append(str(code))

    url = fronturl + ','.join(codelist) + backurl
    with aiohttp.Timeout(timeout):
        async with sessions.get(url) as response:
            logging.info('%s Running' % index)
            num[0] += 1
            future.set_result(await response.text())
            logging.info('now running %s fur' % num[0])
            future.add_done_callback(got_result)


# 通过网易代码并发获取网易api数据
def __getnvalue(*codes, slices=1000, timeout=30, maxdatanum=400000):
    if len(codes) > maxdatanum:
        raise ValueError('Too many code input: %s,max input data num %s' % (len(codes), maxdatanum))
    task = list()
    dictdata = dict()
    futurelist = list()
    loop = asyncio.get_event_loop()
    lcodes = cut_list(codes, slices=slices)
    num = [0, len(lcodes), len(lcodes)]
    with aiohttp.ClientSession(loop=loop) as session:
        for index, ncodes in enumerate(lcodes):
            futurelist.append(asyncio.Future())
            task.append(asyncio.ensure_future(__asyncgetnvalue(session, futurelist[index], dictdata,
                                                               index, num, *ncodes, timeout=timeout)))
        loop.run_until_complete(asyncio.wait(task))

    logging.info('getnvalue: Total received data number %s' % len(dictdata))
    return dictdata

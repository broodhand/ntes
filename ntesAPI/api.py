# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 12:37:57 2016
@author: Zhao Cheng

Create ntes api
"""
import logging; logging.basicConfig(level=logging.DEBUG)
import asyncio
import aiohttp


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

# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 12:37:57 2016
@author: Zhao Cheng
__version__ = '0.0.3'
Asynchronous getting the restful api datas
"""
import logging; logging.basicConfig(level=logging.DEBUG)
import asyncio
import aiohttp


async def _fetch(session, future_content, url, timeout=1, callback_content=lambda self: logging.info(self),
                 res_type='text', encoding='utf-8'):
    choice = dict(text=lambda self: self.text(encoding=encoding),
                  json=lambda self: self.json(),
                  bytes=lambda self: self.read())
    try:
        with aiohttp.Timeout(timeout):
            async with session.get(url) as res:
                statuscode = res.status
                content = await choice[res_type](res)
                logging.debug('get content:%s' % content)
                if res.status == 200:
                    future_content.set_result(dict(url=url, content=content))
                    callback_content(content)
                    return dict(url=url, status=statuscode)
                else:
                    future_content.set_result(dict(url=url, content=None))
                    return dict(url=url, status=statuscode)
    except asyncio.TimeoutError:
        future_content.set_result(dict(url=url, content=None))
        return dict(url=url, status=408)


async def _retry(session, future_content, url, callback_result=lambda self: logging.info(self),
                 retry_times=3, **kwargs):
    retry = 0
    result = dict()
    while retry <= retry_times:
        result = await _fetch(session, future_content, url, **kwargs)
        status = result['status']
        if status == 200:
            result['retry'] = retry
            callback_result(result)
            return result
        else:
            retry += 1
    result['retry'] = retry
    callback_result(result)
    return result


async def _semaphore(session, future, *urls, semaphore=20, **kwargs):
    result_list = list()
    future_content_list = list()
    sem = asyncio.Semaphore(semaphore)
    for url in urls:
        future_content = asyncio.Future()
        future_content_list.append(future_content)
        with (await sem):
            result_list.append(await _retry(session, future_content, url, **kwargs))
    future.set_result(future_content_list)
    return result_list


def get_urls(*urls, **kwargs):
    loop = asyncio.get_event_loop()
    future_content_list = asyncio.Future()
    with aiohttp.ClientSession(loop=loop) as session:
        future = asyncio.ensure_future(_semaphore(session, future_content_list, *urls, **kwargs))
        loop.run_until_complete(future)
    result_future_content_list = future_content_list.result()
    result_list = future.result()
    content_list = list()
    for fur in result_future_content_list:
        content_list.append(fur.result())
    loop.close()
    return dict(content_list=content_list, result_list=result_list)

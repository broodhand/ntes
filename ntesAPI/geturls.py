# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 12:37:57 2016
@author: Zhao Cheng
__version__ = '0.3.0'
Asynchronous getting the restful api datas
"""
import logging; logging.basicConfig(level=logging.INFO)
import asyncio
import aiohttp
import uuid
import time

namespace = uuid.uuid1()


async def _fetch(session, future_content, url, timeout=1, log_content=lambda self: logging.info(self),
                 filter_content=lambda self: self, res_type='text', encoding='utf-8'):
    "To asynchronous getting a url's data"
    choice = dict(text=lambda self: self.text(encoding=encoding),
                  json=lambda self: self.json(),
                  bytes=lambda self: self.read())
    now_stamp = int(time.time())
    now_stand = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now_stamp))
    global namespace
    uuid_name = '%s/%s' % (url, now_stamp)
    myuuid = uuid.uuid3(namespace, uuid_name).hex
    set_result_fail = dict(url=url, status=408, time=now_stand, uuid=myuuid)
    try:
        with aiohttp.Timeout(timeout):
            try:
                async with session.get(url) as res:
                    statuscode = res.status
                    content = await choice[res_type](res)
                    set_content = filter_content(dict(content=content, uuid=myuuid))
                    set_result_success = dict(url=url, status=statuscode, time=now_stand, uuid=myuuid)
                    if res.status == 200:
                        future_content.set_result(set_content)
                        log_content(set_content)
                    return set_result_success
            except aiohttp.errors.ClientOSError:
                return set_result_fail
    except asyncio.TimeoutError:
        return set_result_fail


async def _retry(session, future_content, url, log_result=lambda self: logging.info(self),
                 filter_result=lambda self: self, retry_times=3, **kwargs):
    "When encountered errors,Retry to get data"
    retry = 0
    result = dict()
    while retry <= retry_times:
        result = await _fetch(session, future_content, url, **kwargs)
        status = result['status']
        if status == 200:
            result['retry'] = retry
            set_result = filter_result(result)
            log_result(set_result)
            return set_result
        else:
            retry += 1
    result['retry'] = retry
    set_result = filter_result(result)
    log_result(set_result)
    future_content.set_result(kwargs['filter_content'](content=None, uuid=result['uuid']))
    return set_result


async def _semaphore(session, future, *urls, semaphore=20, **kwargs):
    "Limit the most number of sessions to getting data "
    result_list = list()
    future_content_list = list()
    sem = asyncio.Semaphore(semaphore)
    for url in urls:
        future_content = asyncio.Future()
        future_content_list.append(future_content)
        with (await sem):
            result = await _retry(session, future_content, url, **kwargs)
            result_list.append(result)
    future.set_result(future_content_list)
    return result_list


def get_urls(*urls, **kwargs):
    """
    To asynchronous getting datas from restful api.
    :param urls: Input a url list for getting datas.
    :param :
            retry_times=3: retry times
            semaphore=20: The max sessions to connect servers at the same time.
            timeout=1: the timeout of sessions
            res_type='text': type of data. 'text':str 'bytes':bytes 'json':auto using json encoder
            encode='utf-8': the data's str code
            log_content=lambda self: logging.info(self): callback function for getting content
            log_result=lambda self: logging.info(self): callback function for getting result log
            filter_content=lambda self: self: To filter api get the data's content
            filter_result=lambda self: self: To filter the result of getting data from api
    :return: A dict have key 'content_list' receiving API datas to a dict.
             It have Another key 'error_list' receiving error log to a dict.
             Content dict have the content of url and uuid for this time connect.
             Error dict have the error of getting url and it's uuid
    """
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
    return dict(content_list=content_list, error_list=result_list)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 13:07:18 2016

@author: Zhao Cheng
"""
import aiohttp
import asyncio


async def fetch(sessions, url):
    with aiohttp.Timeout(10):
        async with sessions.get(url) as response:
            return await response.text()

loop = asyncio.get_event_loop()
result = list()
tasks = list()
with aiohttp.ClientSession(loop=loop) as session:
    task1 = asyncio.ensure_future(fetch(session, 'http://api.money.126.net/data/feed/0204001,money.api'))
    task2 = asyncio.ensure_future(fetch(session, 'http://api.money.126.net/data/feed/1131810,money.api'))
    tasks.append(task1)
    tasks.append(task2)
t = loop.run_until_complete(tasks)
print(t)






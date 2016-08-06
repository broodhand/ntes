# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 12:37:57 2016
@author: Zhao Cheng
__version__ = '0.0.2'
The API for aiohttpAPI
"""
from collections import Iterator
from .client import get_urls, get_url


class Urls(object):
    def __init__(self, urls, **kwargs):
        if isinstance(urls, (list, Iterator)):
            self.urls = urls
        else:
            raise TypeError('<aiohttpAPI.client.Urls> The param urls must input list')

        self.timeout = kwargs.get('timeout', 1)
        self.res_type = kwargs.get('res_type', 'text')
        self.encoding = kwargs.get('encoding', 'utf-8')
        self.retry_session = kwargs.get('retry_session', 3)
        self.callback_function = kwargs.get('callback_function')
        self.filter_function = kwargs.get('filter_function')
        self.semaphore = kwargs.get('semaphore', 20)
        self.retry_failure = kwargs.get('retry_failure', 3)
        self.proc_function = kwargs.get('proc_function')

    def get(self):
        return get_urls(self.urls, timeout=self.timeout, res_type=self.res_type, encoding=self.encoding,
                        retry_session=self.retry_session, callback_function=self.callback_function,
                        filter_function=self.filter_function, semaphore=self.semaphore,
                        retry_failure=self.retry_failure, proc_function=self.proc_function)


class Url(object):
    def __init__(self, *url, **kwargs):
        if isinstance(url, (tuple, str)):
            self.url = url
        else:
            raise TypeError('<aiohttpAPI.client.Urls> The param urls must input string ')

        self.timeout = kwargs.get('timeout', 1)
        self.res_type = kwargs.get('res_type', 'text')
        self.encoding = kwargs.get('encoding', 'utf-8')
        self.retry_session = kwargs.get('retry_session', 3)
        self.callback_function = kwargs.get('callback_function')
        self.filter_function = kwargs.get('filter_function')
        self.semaphore = kwargs.get('semaphore', 20)
        self.retry_failure = kwargs.get('retry_failure', 3)
        self.proc_function = kwargs.get('proc_function')

    def get(self):
        return get_url(*self.url, timeout=self.timeout, res_type=self.res_type, encoding=self.encoding,
                       retry_session=self.retry_session, callback_function=self.callback_function,
                       filter_function=self.filter_function, semaphore=self.semaphore,
                       retry_failure=self.retry_failure, proc_function=self.proc_function)

# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 12:37:57 2016
@author: Zhao Cheng
__version__ = '0.0.9'
Get the data of ntes
"""
import logging
import aiohttpAPI
from .url import make_urls
from .scheme_default import filters as filters_default
from .scheme_default import process as process_default


def get_data(codes, scheme='default', timeout=3, retry_session=3, semaphore=20, retry_failure=3):
    """
    To get the stock data from the ntes api
    :param codes: Must input the codes list , tuple or generator
    :param scheme: the scheme for filter, callback, process
    :param timeout: the session's timeout
    :param retry_session: the session retry time
    :param semaphore: the asyncio number
    :param retry_failure: failure retry times
    :return: The codes' data content list.
    """
    try:
        filters = _Scheme.filter[scheme]
        callback = _Scheme.callback[scheme]
        process = _Scheme.process[scheme]
    except Exception as e:
        logging.warning('<ntesDS.data.get_data> scheme name error %s' % e)
        return False

    try:
        urls = make_urls(codes)
        res = aiohttpAPI.Urls(urls, filter_function=filters, callback_function=callback, proc_function=process,
                              res_type='text', encoding='utf-8', timeout=timeout, retry_session=retry_session,
                              retry_failure=retry_failure, semaphore=semaphore)
        result = res.get()
        return result
    except Exception as e:
        logging.warning('<ntesDS.data.get_data> Getting data error %s' % e)
        return False


class _Scheme(object):
    filter = dict(default=filters_default)
    callback = dict(default=None)
    process = dict(default=process_default)

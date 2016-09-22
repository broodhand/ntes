# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 12:37:57 2016
@author: Zhao Cheng
__version__ = '0.0.11'
Get the data of ntes
"""
import logging
import aiohttpAPI
from base import make_urls as _make_urls
from .scheme_default import filters as filters_default
from .scheme_default import process as process_default
from .scheme_of import filters as filters_of
from .scheme_of import process as process_of
from .scheme_of_general import filters as filters_of_general
from .scheme_of_general import process as process_of_general
from .scheme_of_currency import filters as filters_of_currency
from .scheme_of_currency import process as process_of_currency


def make_urls(codes, slices=1000, prefix='http://api.money.126.net/data/feed/', suffix=',money.api', separator=','):
    """
    To make the url for ntes api
    :param codes:Input codes must be a Iterator
    :param slices: code slices for once inputting url
    :param prefix: ntes api url prefix
    :param suffix: ntes api url suffix
    :param separator: ntes api code separator
    :return: generator for getting data url
    """
    return _make_urls(codes, slices, prefix, suffix, separator)


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
    filter = dict(default=filters_default, of=filters_of, of_general=filters_of_general,
                  of_currency=filters_of_currency)
    callback = dict(default=None, of=None, of_general=None, of_currency=None)
    process = dict(default=process_default, of=process_of, of_general=process_of_general,
                   of_currency=process_of_currency)

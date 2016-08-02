# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 12:37:57 2016
@author: Zhao Cheng
__version__ = '0.0.3'
Get the data of ntes
"""
import logging;logging.basicConfig(level=logging.INFO)
import aiohttpAPI
from .url import make_urls
from .code import of_code_generator
from .scheme_default import filer as filer_default
from .scheme_default import callback as callback_default
from .scheme_default import process as process_default


scheme_dict = {
    'default': {'filter': lambda x:  filer_default(x),
                'callback': lambda x: callback_default(x),
                'process': lambda x: process_default(x)
                }
}


def get_data(codes, scheme='default', **aiohttp_cfg):
    """
    To get the stock data from the ntes api
    :param codes: Must input the codes list , tuple or generator
    :param scheme: the scheme for filter, callback, process
    :param aiohttp_cfg: Pass to aiohttpAPI.get_urls,so the same with it.But default use the following callback function.
                        filer: filter_function = _filer_vaild_content
                        log: log_function = _log_info_error
                        result process: proc_function = _process_result_list_code
    :return: The codes' data content list.
    """
    global scheme_dict
    try:
        filters = scheme_dict[scheme]['filter']
        callback = scheme_dict[scheme]['callback']
        process = scheme_dict[scheme]['process']
    except Exception as e:
        logging.warning('<ntesDS.data> scheme name error')
        raise ValueError(r'<ntesDS.data> scheme name error \r\n error: %s' % e)
    return aiohttpAPI.get_urls(make_urls(codes), filter_function=filters, callback_function=callback,
                               proc_function=process, **aiohttp_cfg)


def of_data(scheme='default', timeout=3, semaphore=20, **kwargs):
    return get_data(of_code_generator(), scheme=scheme, timeout=timeout, semaphore=semaphore, **kwargs)

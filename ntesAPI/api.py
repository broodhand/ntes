# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 12:37:57 2016
@author: Zhao Cheng
__version__ = '0.0.2'
Get the data of ntes
"""
import logging; logging.basicConfig(level=logging.INFO)
import aiohttpAPI
import re
import json
from .tools import generate_merger_codes, make_urls
from .error import ApiError

# a re for matching the ntes result data
re_ntes = re.compile(r"_ntes_quote_callback\((?P<data>.*)\);")


def get_all_data(**kwargs):
    """
    To get the all probability codes' data from ntes api
    :param kwargs: pass to get_data, so the same with it.
    :return: vaild_codes is the codes which can get the data
             result_list is the vaild result list of all codes
    """
    result_list = list()
    vaild_codes = list()
    codes_generator = generate_merger_codes(7)
    try:
        result_list = get_data(codes_generator, **kwargs)
    except Exception:
        logging.warning("<ntesAPI.api.get_all_data>  Call get_data error.")
        raise ApiError("<ntesAPI.api.get_all_data>  Get all data failure")
    else:
        for result in result_list:
            for k in result.keys():
                vaild_codes.append(k)
    finally:
        logging.info('get_all_data() completely done')
        return vaild_codes, result_list


def get_data(codes, **kwargs):
    """
    To get the stock data from the ntes api
    :param codes: Must input the codes list , tuple or generator
    :param kwargs: Pass to aiohttpAPI.get_urls,so the same with it.But default use the following callback function.
                   filer: filter_function = _filer_vaild_content
                   log: log_function = _log_info_error
                   result process: proc_function = _process_result_list_code
    :return: The codes' data content list.
    """
    urls = make_urls(codes)
    result_list = aiohttpAPI.get_urls(urls, filter_function=_filer_vaild_content, log_function=_log_info_error,
                                      proc_function=_process_result_list_code, **kwargs)
    return result_list


def _filer_vaild_content(content):
    """
    Call back function for the aiohttpAPI.get_urls to filer every piece of result content from the ntes api.
    :param content: The result input.It's a str like"_ntes_quote_callback({...})". "{...}" is the json str.
    :return: discard result which have no the "content" key or the "content" key have no content.
    """
    if content['content'] is not None:
        json_str = re_ntes.match(content['content']).group('data')
        content_dict = json.loads(json_str)
        if len(content_dict) == 0:
            return None
        else:
            return content_dict
    else:
        return None


def _log_info_error(log):
    """
    Call back function for the aiohttpAPI.get_urls to log the content of every piece of result from the ntes api.
    :param log: Every result input for log.
    :return: If the key "status" is 200,discard this piece of result.So only log error result
    """
    if log['status'] != 200:
        logging.info(log)


def _process_result_list_code(result_list):
    """
    Call back function for precessing the result list.Get the single result for a code.
    :param result_list: The list of the every request's result.
    :return:The code's content list
    """
    new_result_list = list()
    for result in result_list:
        for k, v in result.items():
            new_dict = dict()
            new_dict[k] = v
            new_result_list.append(new_dict)
    return new_result_list




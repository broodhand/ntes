# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 12:37:57 2016
@author: Zhao Cheng
__version__ = '0.0.1'
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
    urls = make_urls(codes)
    result_list = aiohttpAPI.get_urls(urls, filter_function=_filer_content, log_function=_log_error,
                                      proc_function=_process_result, **kwargs)
    return result_list


def _filer_content(content):
    if content['content'] is not None:
        json_str = re_ntes.match(content['content']).group('data')
        content_dict = json.loads(json_str)
        if len(content_dict) == 0:
            return None
        else:
            return content_dict
    else:
        return None


def _log_error(log):
    if log['status'] != 200:
        logging.info(log)


def _process_result(result_list):
    new_result_list = list()
    for result in result_list:
        for k, v in result.items():
            new_dict = dict()
            new_dict[k] = v
            new_result_list.append(new_dict)
    return new_result_list




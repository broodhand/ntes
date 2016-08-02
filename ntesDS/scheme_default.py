# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 12:37:57 2016
@author: Zhao Cheng
__version__ = '0.0.1'
Scheme default
"""
import logging
import re
import json
from functools import reduce

re_ntes = re.compile(r"_ntes_quote_callback\((?P<data>.*)\);")


def filer(content):
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


def callback(log):
    """
    Call back function for the aiohttpAPI.get_urls to log the content of every piece of result from the ntes api.
    :param log: Every result input for log.
    :return: If the key "status" is 200,discard this piece of result.So only log error result
    """
    if log['status'] != 200:
        logging.warning(log)


def process(result_list):
    """
    Call back function for precessing the result list.Get the single result for a code.
    :param result_list: The list of the every request's result.
    :return:The code's content list
    """
    return reduce(lambda x, y: dict(x, **y), result_list)

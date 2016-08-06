# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 12:37:57 2016
@author: Zhao Cheng
__version__ = '0.0.4'
Scheme default
"""
import re
import json
from functools import reduce


def filters(content):
    """
    Call back function for the aiohttpAPI.get_urls to filer every piece of result content from the ntes api.
    :param content: The result input.It's a str like"_ntes_quote_callback({...})". "{...}" is the json str.
    :return: discard result which have no the "content" key or the "content" key have no content.
    """
    if isinstance(content, dict):
        if content.get('content') is not None:
            json_str = _Re.ntes.match(content['content']).group('data')
            content_dict = json.loads(json_str)
            if len(content_dict) == 0:
                return None
            else:
                return content_dict
        else:
            return None
    else:
        return None


def process(result_list):
    """
    Call back function for precessing the result list.Get the single result for a code.
    :param result_list: The list of the every request's result.
    :return:The code's content list
    """
    if result_list:
        return reduce(lambda x, y: dict(x, **y), result_list)
    else:
        return None


class _Re(object):
    ntes = re.compile(r"_ntes_quote_callback\((?P<data>.*)\);")
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 12:37:57 2016
@author: Zhao Cheng
__version__ = '0.1.0'
Tools for ntes
"""
import logging; logging.basicConfig(level=logging.INFO)
import base
from collections import Iterator


def _make_url(*codes, input_max=1000, prefix='http://api.money.126.net/data/feed/', suffix=',money.api', separator=','):
    """
    To make the ntes api url address for restful input to ntes API
    """
    code_list = list()

    if len(codes) > input_max:
        raise ValueError('<ntesDS.base> Codes input too much.(%s > %s)' % (len(codes), input_max))

    if codes:
        for code in codes:
            code_list.append(str(code))
        return prefix + separator.join(code_list) + suffix


def make_urls(codes, slices=1000):
    """
    To make the url for ntes api
    :param codes:Input codes must be a Iterator
    :param slices: code slices for once inputting url
    :return: generator for getting data url
    """
    if isinstance(codes, (Iterator, list, tuple)):
        code_generator = base.cut_seq(codes, slices=slices)
        for code_tuple in code_generator:
            yield _make_url(*code_tuple, input_max=slices)
    else:
        raise TypeError('Must input a generator,list or tuple')



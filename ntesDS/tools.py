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


def make_url(*codes, codes_max=1000):
    """
    To make the ntes api url address for restful input to ntes API
    """
    _fronturl = 'http://api.money.126.net/data/feed/'
    _backurl = ',money.api'
    _codelist = list()
    logging.debug('<ntesDS.tools.mak_ntes_url>Input code number %s' % len(codes))
    if len(codes) == 0:
        raise ValueError('Must input code')
    if len(codes) > codes_max:
        raise ValueError('Codes input too much.(%s > %s)' % (len(codes), codes_max))
    for code in codes:
        _codelist.append(str(code))
    return _fronturl + ','.join(_codelist) + _backurl


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
            yield make_url(*code_tuple, codes_max=slices)
    else:
        raise TypeError('Must input a generator,list or tuple')


def generate_codes(dit):
    "Generate the codes by digit,Not merge"
    for x in range(10 ** dit):
        yield str(x).zfill(dit)


def generate_merger_codes(dit):
    "Generate the codes by digit ,Merge code which is less code digit."
    for digit in range(dit):
        for code in generate_codes(digit+1):
            yield code


def get_all_codes_urls():
    "TO make the all probability codes' urls"
    codes_generator = generate_merger_codes(7)
    urls_generator = make_urls(codes_generator)
    return urls_generator

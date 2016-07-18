# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 12:37:57 2016
@author: Zhao Cheng
__version__ = '0.0.6'
Tools for ntes
"""
import logging; logging.basicConfig(level=logging.DEBUG)
import base
from collections import Iterator


def make_ntes_url(*codes, codes_max=1000):
    "To make the url address for restful input to ntes API"
    _fronturl = 'http://api.money.126.net/data/feed/'
    _backurl = ',money.api'
    _codelist = list()
    logging.info('Input code number %s' % len(codes))
    if len(codes) == 0:
        raise ValueError('Must input code')
    if len(codes) > codes_max:
        raise ValueError('Codes input too much.(%s > %s)' % (len(codes), codes_max))
    for code in codes:
        _codelist.append(str(code))
    return _fronturl + ','.join(_codelist) + _backurl


def make_urls(generator, slices=1000):
    if isinstance(generator, Iterator):
        code_generator = base.cut_seq(generator, slices=slices)
        for code_tuple in code_generator:
            yield make_ntes_url(*code_tuple, codes_max=slices)
    else:
        raise TypeError('Must input a generator')


def generate_codes(dit):
    "Generate the codes by digit,Not "
    for x in range(10 ** dit):
        yield str(x).zfill(dit)


def generate_merger_codes(dit):
    "Generate the codes by digit ,Merge code less digit."
    for digit in range(dit):
        for code in generate_codes(digit+1):
            yield code


def get_all_codes_urls():
    codes_generator = generate_merger_codes(7)
    urls_generator = make_urls(codes_generator)
    return urls_generator

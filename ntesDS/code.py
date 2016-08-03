# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 12:37:57 2016
@author: Zhao Cheng
__version__ = '0.2.0'
Code lib
"""
import logging;logging.basicConfig(level=logging.DEBUG)
from .data import get_data


def _generate_code(dit):
    """Generate the codes by digit"""
    for x in range(10 ** dit):
        yield str(x).zfill(dit)


def of_code_generator():
    """
    Get ntes offfund codes
    :return: codes generator
    """
    for code in _generate_code(6):
        yield code


def sh_code_generator():
    """
    Get ntes sh codes
    :return: codes generator
    """
    for code in _generate_code(6):
        yield '0' + code


def sz_code_generator():
    """
    Get ntes sz codes
    :return: codes generator
    """
    for code in _generate_code(6):
        yield '1' + code

generator = {
    'OF': of_code_generator,
    'SH': sh_code_generator,
    'SZ': sz_code_generator
}


class Codes(object):
    def __init__(self, codes_type, scheme='default', timeout=1, retry_session=3, semaphore=20, retry_failure=3):
        global generator
        if codes_type in generator.keys():
            self._generator = generator[codes_type]
        else:
            raise CodeError('Please select OF,SZ or SH')
        self._scheme = scheme
        self._timeout = timeout
        self._retry_session = retry_session
        self._semaphore = semaphore
        self._retry_failure = retry_failure
        self._init = False
        self._data_tuple = None
        self._data = None
        self._report = None
        self._num = None
        self._codes = None
        self._content = None

    def init(self):
        if self._init:
            raise CodeError('Already init')

        self._data_tuple = get_data(self._generator, scheme=self._scheme, timeout=self._timeout,
                                    retry_session=self._retry_session, semaphore=self._semaphore,
                                    retry_failure=self._retry_failure)
        if self._data_tuple:
            self._data = self._data_tuple[0]
            self._report = self._data_tuple[1]
            self._num = len(self._data)
            self._codes = self._data.keys()
            self._content = self._data.values()

        self._init = True

    @property
    def data(self):
        if self._init:
            return self._data
        else:
            raise CodeError('Need init first')

    @property
    def report(self):
        if self._init:
            return self._report
        else:
            raise CodeError('Need init first')

    @property
    def num(self):
        if self._init:
            return self._num
        else:
            raise CodeError('Need init first')

    @property
    def codes(self):
        if self._init:
            return self._codes
        else:
            raise CodeError('Need init first')

    @property
    def content(self):
        if self._init:
            return self._content
        else:
            raise CodeError('Need init first')


class CodeError(Exception):
    pass

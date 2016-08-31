# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 12:37:57 2016
@author: Zhao Cheng
__version__ = '0.2.4'
Code lib
"""


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


def sh_index_code_generator():
    """
    Get ntes sh index codes
    :return: codes generator
    """
    for code in _generate_code(3):
        yield '0000' + code


def into_standard(code):
    if len(code) == 6 and code.isdigit():
        return code+'.OF'
    if len(code) == 7 and code.isdigit():
        if code[0] == '0':
            return code[1:] + '.SH'
        elif code[0] == '1':
            return code[1:] + '.SZ'


def from_standard(code):
    if isinstance(code, str):
        if code.endswith('.OF'):
            return code[:-3]
        elif code.endswith('.SH'):
            return '0' + code[:-3]
        elif code.endswith('.SZ'):
            return '1' + code[:-3]


class Generator(object):
    function = {
        'OF': of_code_generator,
        'SH': sh_code_generator,
        'SZ': sz_code_generator,
        'SH_INDEX': sh_index_code_generator
    }
    all = function.keys()


class Convert(object):
    callback = {
        'ntes': lambda x: x,
        'standard': into_standard
    }


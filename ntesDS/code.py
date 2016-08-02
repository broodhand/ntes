# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 12:37:57 2016
@author: Zhao Cheng
__version__ = '0.1.1'
Code lib
"""
import logging; logging.basicConfig(level=logging.INFO)
from .data import get_data


def _generate_code(dit):
    "Generate the codes by digit"
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


def of_data(scheme='default', timeout=3, semaphore=20, **kwargs):
    return get_data(of_code_generator(), scheme=scheme, timeout=timeout, semaphore=semaphore, **kwargs)




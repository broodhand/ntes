# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 12:37:57 2016
@author: Zhao Cheng
__version__ = '0.0.1'
Scheme of otc fund.
"""
import hashlib
from .code import into_standard
from .scheme_default import filters as filters_default
from .scheme_default import process as process_default


def md5_currency(code, curnav_001, nav):
    msg = '%s/%s/%s' % (code, curnav_001, nav)
    md5 = hashlib.md5(msg.encode())
    return md5.hexdigest()


def filters(content):
    return filters_default(content)


def process(result_list):
    result = process_default(result_list)
    result_of = dict()
    for code, content in result.items():
        if ('curnav_001' in content) and ('nav' in content):
            code_currency = into_standard(str(code))
            curnav_001_currency = content.get('curnav_001')
            nav_currency = content.get('nav')
            md5 = md5_currency(code_currency, curnav_001_currency, nav_currency)
            result_of.update({code: {'code.standard': code_currency,
                                     'curnav_001.currency': curnav_001_currency,
                                     'nav.currency': nav_currency,
                                     'md5': md5
                                     }
                              })
    return result_of

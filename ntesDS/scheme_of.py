# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 12:37:57 2016
@author: Zhao Cheng
__version__ = '0.0.1'
Scheme of
"""
import hashlib
from .code import into_standard
from .scheme_default import filters as filters_default
from .scheme_default import process as process_default


def filters(content):
    return filters_default(content)


def process(result_list):
    result = process_default(result_list)
    result_of = dict()
    for code, content in result.items():
        if content.get('TYPENAME1') in ('场内基金', '场外基金'):
            navdate = content.get('navdate')
            nav = content.get('nav')
            pchg = content.get('pchg')
            if navdate or nav or pchg:
                md5 = md5_of(code, navdate, nav, pchg)
                result_of.update({code: {'code.standard': into_standard(str(code)),
                                         'navdate.of': navdate,
                                         'nav.of': nav,
                                         'pchg.of': pchg,
                                         'md5': md5
                                         },
                                  })
        elif content.get('TYPENAME1') == '货币式':
            curnav_001 = content.get('curnav_001')
            nav = content.get('nav')
            if curnav_001 or nav:
                md5 = md5_currency(code, curnav_001, nav)
                result_of.update({code: {'code.standard': into_standard(str(code)),
                                         'curnav_001.currency': curnav_001,
                                         'nav.currency': nav,
                                         'md5': md5
                                         }
                                  })
    return result_of


def md5_of(code, navdate, nav, pchg):
    msg = '%s/%s/%s/%s' % (code, navdate, nav, pchg)
    md5 = hashlib.md5(msg.encode())
    return md5.hexdigest()


def md5_currency(code, curnav_001, nav):
    msg = '%s/%s/%s' % (code, curnav_001, nav)
    md5 = hashlib.md5(msg.encode())
    return md5.hexdigest()

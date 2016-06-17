#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2016/6/17 13:11

@project: Grandet
@version: 0.99
@file: test.py
@author: SPBG Co.,Ltd. ing / 北京正民惠浩投资管理有限公司 ing
@contact: ing@spbgcapital.com
@site: http://www.spbgcapital.net
"""
PACKAGENAME = 'homepage'
MODELNAME = 'layout'


def fn(self):
    print('ok')

A = type('Hello', (object,), dict(hello=fn))



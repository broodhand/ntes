#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2016/6/16 11:07
@file: __init__.py.py
@author: SPBG Co.,Ltd. ing / 北京正民惠浩投资管理有限公司 ing
@contact: ing@spbgcapital.com
@site: http://www.spbgcapital.net
"""
from .tools import merge, cut_seq

__version__ = '0.1.0'
VERSION = tuple(map(int, __version__.split('.')))

__all__=['merge', 'cut_seq']
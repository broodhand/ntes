#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2016/6/18 15:26

@project: Grandet
@version: 0.99
@file: testxxx.py
@author: SPBG Co.,Ltd. ing / 北京正民惠浩投资管理有限公司 ing
@contact: ing@spbgcapital.com
@site: http://www.spbgcapital.net
"""
import inspect

class a(object):
    def __init__(self):
        self.name = self.__class__.__name__
        self.modulename = __name__


    def show(self):
        print(self.name, self.modulename, self.modulename1)
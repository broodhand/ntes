#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on 6/23/16 2:06 PM

@file:view.py
@author: SPBG Co.,Ltd. ..ing 北京正民惠浩投资管理有限公司 ..ing
"""
view = [('home.html', '{"navigation": [{"caption": "公司简介","href": "／introduce"},{"caption": "项目情况","href": "／profile"}],"subnavigation": [{"caption": "github","href": "http://www.github.com"},{"caption": "Wechat","href": "http://www.wechat.com"}]}')]


def getview(types='json'):
    if types == 'json':
        return view





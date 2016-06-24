#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on 6/23/16 2:06 PM

@file:view.py
@author: SPBG Co.,Ltd. ..ing 北京正民惠浩投资管理有限公司 ..ing
"""
import logging; logging.basicConfig(level=logging.INFO)
import json
from database.mysqldb import create_pool, select

homepara = {'navigation': [{'caption': '简介', 'href': '/project'},
  {'caption': '业务', 'href': '/business'},
  {'caption': '项目', 'href': '/project'},
  {'caption': '文档', 'href': '/document'},
  {'caption': '案例', 'href': '/case'},
  {'caption': '联系', 'href': '/contack'}],
 'subnavigation': [{'caption': 'GitHub',
   'href': 'http://www.github.com/broodhand'},
  {'caption': '反馈', 'href': '/feedback'},
  {'caption': '更新', 'href': '/log'},
  {'caption': '论坛', 'href': '/luntan'}]}

renderpara = list()
renderpara.append(('home', json.dumps(homepara)))


def getrenderpara(types='json'):
    global renderpara
    if types == 'json':
        return renderpara
    if types =='mysql':
        create_pool(file='website.cfg')
        result = select('select func,renderkw from spbg_webapp', None)
        return result




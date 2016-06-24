#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2016/6/15 22:52

@project: spbgcapital homepage
@version: 0.99
@file: spbgcapital.py
@author: SPBG Co.,Ltd. ing / 北京正民惠浩投资管理有限公司 ing
@contact: ing@spbgcapital.com
@site: http://www.spbgcapital.com
"""
import logging; logging.basicConfig(level=logging.INFO)
import json
import sys
from flask import Flask
from jinja2 import Environment, PackageLoader
from spbg_webapp.www.renderpara import getrenderpara


# 获取网站渲染所有参数的类
class Website(object):
    def __init__(self, view):
        for row in view:
            logging.info(row[1])
            logging.info(json.loads(row[1].decode()))
            setattr(self, row[0], json.loads(row[1].decode()))


# ---Start---
app = Flask(__name__)  # 初始化Flask
env = Environment(loader=PackageLoader('template', '/'))  # 初始化jinja2环境
para = getrenderpara(types='mysql')
web = Website(getrenderpara(types='mysql'))  # 初始化网页对象


@app.route('/', methods=['GET', 'POST'])
def home():
    funcname = sys._getframe().f_code.co_name
    viewname = funcname + '.html'
    renderpara = getattr(web, funcname)
    template = env.get_template(viewname)
    view = template.render(**renderpara)
    return view

if __name__ == '__main__':
    app.run()


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
import logging
from flask import Flask
from jinja2 import Environment, PackageLoader
from database.sqlalchemydb import SqlalchemyDB
from spbg_webapp.www.orm import *

logging.basicConfig(level=logging.INFO)


# 获取网站渲染所有参数的类
class Website(object):
    page = ['home.html']

    def __init__(self, sqlsession):
        self.page = Website.page
        self.func = dict()
        self.cls = dict()
        for file in self.page:
            self.func[file] = file.split('.')[0]
            self.cls[file] = file.split('.')[0].capitalize()
            myobj = eval(self.cls[file]+'()')
            renderkw = myobj.get_render_kw(sqlsession)
            setattr(self, self.func[file], renderkw)

app = Flask(__name__)  # 初始化Flask
env = Environment(loader=PackageLoader('template', '/'))  # 初始化jinja2环境

# 初始化jinja2渲染参数对象
session = SqlalchemyDB('website.cfg').getsession()  # 获取sqlalchemy的session
web = Website(session)  # 初始化网页对象


@app.route('/', methods=['GET', 'POST'])
def home():
    template = env.get_template('home.html')
    view = template.render(**web.home)
    logging.info(view)
    return view


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

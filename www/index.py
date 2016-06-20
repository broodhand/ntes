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
from www.homepage.layout import Layout
from database.sqlalchemydb import SqlalchemyDB

logging.basicConfig(level=logging.INFO)
session = SqlalchemyDB('index.cfg').getsession()  # 获取sqlalchemy的session
app = Flask(__name__)  # 初始化Flask
env = Environment(loader=PackageLoader('homepage', 'templates'))

layout = Layout()
kw = dict()

for (arg, obj) in layout.ormDict.items():
    kw[arg] = session.query(obj).order_by('seq').all()


@app.route('/', methods=['GET', 'POST'])
def home():
    template = env.get_template('index.html')
    view = template.render(**kw)
    logging.info(view)
    return view

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

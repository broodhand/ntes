#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2016/6/26 16:57

@project: Grandet
@version: 0.99
@file: test.py.py
@author: SPBG Co.,Ltd. ing / 北京正民惠浩投资管理有限公司 ing
@contact: ing@spbgcapital.com
@site: http://www.spbgcapital.net
"""
from flask import Flask
from jinja2 import Environment, PackageLoader

app = Flask(__name__)  # 初始化Flask
env = Environment(loader=PackageLoader('template', '/'))  # 初始化jinja2环境


@app.route('/', methods=['GET', 'POST'])
def home():
    template = env.get_template('testechart.html')
    view = template.render()
    print(view)
    return view

if __name__ == '__main__':
    app.run()
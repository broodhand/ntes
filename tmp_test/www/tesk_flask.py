#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2016/6/9 19:54

@project: Grandet
@version: 0.99
@file: tesk_flask.py
@author: SPBG Co.,Ltd. ing / 北京正民惠浩投资管理有限公司 ing
@contact: ing@spbgcapital.com
@site: http://www.spbgcapital.net
"""

from flask import Flask
from flask import request
from flask import render_template

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2016/6/19 14:24

@project: Grandet
@version: 0.99
@file: xiaxia.py
@author: SPBG Co.,Ltd. ing / 北京正民惠浩投资管理有限公司 ing
@contact: ing@spbgcapital.com
@site: http://www.spbgcapital.net
"""
a = int(input('please input a:'))
b = int(input('please input b:'))
e = float(input('please input e:'))
c = int(input('please input c:'))
d = int(input('please input d:'))
f = float(input('please input f:'))
x = (e*d/b-f)/(a*d/b-c)
y = (e*c/a-f)/(b*c/a-d)
print('x is %s,y is %s' % (round(x,2),round(y,2)))


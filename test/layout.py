#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2016/6/16 23:49

@project: Homepage
@version: 0.99
@file: base.py
@author: SPBG Co.,Ltd. ing / 北京正民惠浩投资管理有限公司 ing
@contact: ing@spbgcapital.com
@site: http://www.spbgcapital.net
"""
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()  # ORM表对象


class Navigation(Base):
    __tablename__ = 'homepage_layout_navigation'
    seq = Column(Integer, primary_key=True)
    caption = Column(String(20))
    href = Column(String(255))


class Subnavigation(Base):
    __tablename__ = 'homepage_layout_subnavigation'
    seq = Column(Integer, primary_key=True)
    caption = Column(String(20))
    href = Column(String(255))

args = {'navigation': Navigation, 'subnavigation': Subnavigation}

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 13:07:18 2016

@author: Zhao Cheng
"""

import datasource

nets = datasource.NetsTickData('204001')
nets.value_cachestream2()


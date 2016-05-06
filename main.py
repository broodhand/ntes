# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 11:02:14 2016

@author:Zhao Cheng
"""

import database
import datasource

td = database.rediscallback
n = datasource.NetsTickData('204001')

n.value_stream(callback_func=td)


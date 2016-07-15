# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 12:37:57 2016
@author: Zhao Cheng
__version__ = '0.1.1'
To config logstash
"""
import logging; logging.basicConfig(level=logging.INFO)
import config_default
import base

logstash = config_default.logstash

try:
    from . import config_override
    base.merge(logstash, config_overrides.logstash)
    logging.info('Get the config_override')
except ImportError:
    logging.info('config_override not exist')







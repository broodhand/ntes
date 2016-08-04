# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 12:37:57 2016
@author: Zhao Cheng
__version__ = '0.0.1'
To config diting (谛听)
"""
import logging
import config_default
import base

diting_default = config_default.diting

try:
    from .config_override import diting as diting_override
    diting = base.merge(diting_default, diting_override)
    logging.info('Get the config_override')
except ImportError:
    logging.info('config_override not exist')
    diting = diting_default






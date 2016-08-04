# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 12:37:57 2016
@author: Zhao Cheng
__version__ = '0.0.1'
trading days api for diting I(谛听1)
"""
import logging
from . import config
from base import tradingdays_stop
from base import Set, Str
from config_default import ConfigError
from datetime import date
import redisDB


try:
    tradingdays_cfg = config.diting['tradingdays']  # Get config from config.py
    redis_cfg = tradingdays_cfg['redisDB']
    keyname_data = tradingdays_cfg['keyname_data']
    keyname_status = tradingdays_cfg['keyname_status']
    db_data = tradingdays_cfg['db_data']
    db_status = tradingdays_cfg['db_status']
except Exception as e:
    raise ConfigError('<ditingI.tradingdays> Read config error')


def init_tradingdays():
    global redis_cfg, keyname_data, keyname_status, db_data, db_status
    redis_cfg_data = dict(redis_cfg, db=db_data)
    redis_cfg_status = dict(redis_cfg, db=db_status)

    try:
        stop_days = Set(map(lambda x: x.toordinal(), tradingdays_stop()))
        result1 = stop_days.redis_mapping(keyname_data, **redis_cfg_data)
        logging.info('<ditingI.tradingdays.init_tradingdays> add redis.%s %d' % (keyname_data, result1))
        status = Str('True')
        result2 = status.redis_set(keyname_status, **redis_cfg_status)
        logging.info('<ditingI.tradingdays.init_tradingdays> Set redis.%s %d' % (keyname_status, result2))
        logging.info('<ditingI.tradingdays.init_tradingdays> Initial trading days system ok.')
        return True
    except Exception as e:
        logging.info('<ditingI.tradingdays.init_tradingdays> Unknown error %s' % e)
        redisDB.delkey(keyname_data, **redis_cfg_data)
        redisDB.delkey(keyname_status, **redis_cfg_status)
        return False


def is_today_trade():
    global redis_cfg, keyname_data, keyname_status, db_data, db_status

    today = date.today().toordinal()
    redis_cfg_data = dict(redis_cfg, db=db_data)
    redis_cfg_status = dict(redis_cfg, db=db_status)

    if redisDB.get(keyname_status, **redis_cfg_status) == 'True':
        if redisDB.sismember(keyname_data, today, **redis_cfg_data):
            return False
        else:
            return True
    else:
        return


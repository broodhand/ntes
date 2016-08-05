# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 12:37:57 2016
@author: Zhao Cheng
__version__ = '0.0.4'
trading days api for diting I(谛听1)
"""
import logging
from . import config
from base import tradingdays_stop
from base import Set, Str
from config_default import ConfigError
from datetime import date
import redisDB


def init_tradingdays():
    redis_cfg_data = dict(_Kwargs.redis_cfg, db=_Kwargs.db_data)
    redis_cfg_status = dict(_Kwargs.redis_cfg, db=_Kwargs.db_status)

    try:
        stop_days = Set(map(lambda x: x.toordinal(), tradingdays_stop()))
        result1 = stop_days.redis_mapping(_Kwargs.keyname_data, **redis_cfg_data)
        logging.info('<ditingI.tradingdays.init_tradingdays> add redis.%s %d' % (_Kwargs.keyname_data, result1))
        status = Str('True')
        result2 = status.redis_set(_Kwargs.keyname_status, **redis_cfg_status)
        logging.info('<ditingI.tradingdays.init_tradingdays> Set redis.%s %d' % (_Kwargs.keyname_status, result2))
        logging.info('<ditingI.tradingdays.init_tradingdays> Initial trading days system ok.')
        return True
    except Exception as e:
        logging.info('<ditingI.tradingdays.init_tradingdays> Unknown error %s' % e)
        redisDB.delkey(_Kwargs.keyname_data, **redis_cfg_data)
        redisDB.delkey(_Kwargs.keyname_status, **redis_cfg_status)
        return False


def is_trade_day(input_date=None):
    if input_date is None:
        input_date = date.today().toordinal()
    elif isinstance(input_date, date):
        input_date = input_date.toordinal()
    else:
        return False

    redis_cfg_data = dict(_Kwargs.redis_cfg, db=_Kwargs.db_data)
    redis_cfg_status = dict(_Kwargs.redis_cfg, db=_Kwargs.db_status)

    if redisDB.get(_Kwargs.keyname_status, **redis_cfg_status) == 'True':
        if redisDB.sismember(_Kwargs.keyname_data, input_date, **redis_cfg_data):
            return False
        else:
            return True
    else:
        return


class _Kwargs(object):
    try:
        tradingdays_cfg = config.diting['tradingdays']  # Get config from config.py
        redis_cfg = tradingdays_cfg['redisDB']
        keyname_data = tradingdays_cfg['keyname_data']
        keyname_status = tradingdays_cfg['keyname_status']
        db_data = tradingdays_cfg['db_data']
        db_status = tradingdays_cfg['db_status']
    except Exception as e:
        raise ConfigError('<ditingI.tradingdays> Read config error')

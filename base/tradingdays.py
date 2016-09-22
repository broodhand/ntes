# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 12:37:57 2016
@author: Zhao Cheng
__version__ = '0.0.4'
This a lib of trade date tools for the system
"""
import logging; logging.basicConfig(level=logging.INFO)
from datetime import date, timedelta
from functools import reduce


def _get_weekends(start_date, end_date):
    dates = list()
    date_delta = end_date - start_date
    for i in range(date_delta.days + 1):
        date_item = start_date + timedelta(i)
        weekday = date_item.weekday()
        if weekday == 5 or weekday == 6:
            dates.append(date_item)
    return tuple(dates)


def _tradingdays_stop_2016():
    weekends = _get_weekends(date(2016, 1, 1), date(2016, 12, 31))
    new_year = (date(2016, 1, 1), date(2016, 1, 2), date(2016, 1, 3))
    spring_festival = (date(2016, 2, 7), date(2016, 2, 8), date(2016, 2, 9), date(2016, 2, 10), date(2016, 2, 11),
                       date(2016, 2, 12), date(2016, 2, 13))
    qingming_festival = (date(2016, 4, 2), date(2016, 4, 3), date(2016, 4, 4))
    labour_day = (date(2016, 4, 30), date(2016, 5, 1), date(2016, 5, 2))
    duanwu_festival = (date(2016, 6, 9), date(2016, 6, 10), date(2016, 6, 11))
    zhongqiu_festival = (date(2016, 9, 15), date(2016, 9, 16), date(2016, 9, 17))
    national_day = (date(2016, 10, 1), date(2016, 10, 2), date(2016, 10, 3), date(2016, 10, 4), date(2016, 10, 5),
                    date(2016, 10, 6), date(2016, 10, 7))
    return reduce(lambda x, y: set(x).union(set(y)), [weekends, new_year, spring_festival, qingming_festival,
                                                      labour_day, duanwu_festival, zhongqiu_festival,
                                                      national_day])


def tradingdays_stop():
    year = date.today().year
    if year in _Kwargs.stop.keys():
        return _Kwargs.stop[year]()
    else:
        raise TradingdaysError('<base.tradingdays.tradingdays_stop> Have no this year function')


def istradingday(day):
    stopdays = tradingdays_stop()
    if day > _Kwargs.end or day < _Kwargs.start:
        raise TradingdaysError("<base.tradingdays.istradingday> Out of the data date range")
    if day in stopdays:
        return False
    else:
        return True


class TradingdaysError(Exception):
    pass


class _Kwargs(object):
    start = date(2016, 1, 1)
    end = date(2016, 12, 31)
    stop = {2016: _tradingdays_stop_2016}





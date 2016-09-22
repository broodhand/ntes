"""
Created on Wed Mar 23 12:37:57 2016
@author: Zhao Cheng
__version__ = '0.1.0'
"""

redisDB = {'socket_connect_timeout': 3}


logstash = {
    'redisAPI_config': {
        'socket_connect_timeout': 3,
        'db': 0
    },
    'logstash_listname': 'logstash-list'
}

diting = {
    'tradingdays': {'redisDB': redisDB},

}


class ConfigError(Exception):
    pass

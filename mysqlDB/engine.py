import logging; logging.basicConfig(level=logging.DEBUG)
import mysql.connector


def create_engine(user, password, database, host='localhost', port=3306, **kw):
    params = dict(user=user, password=password, database=database, host=host, port=port)
    defaults = dict(use_unicode=True, charset='utf8', collation='utf8_general_ci', autocommit=False)
    for (k, v) in defaults.items():
        params[k] = kw.pop(k, v)
    params.update(kw)
    params['buffered'] = True
    return _Engine(lambda: mysql.connector.connect(**params))


class _Engine(object):
    def __init__(self, connect):
        self._connect = connect

    def connect(self):
        return self._connect()

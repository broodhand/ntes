from .connect import (connection, with_connection, with_connect)
from .api import (pipeline, flushall, flushdb, smembers, exists, keytype, sismember, keys, delkey, sadd, scard, sdiff,
                  sdiffstore, sinter, sinterstore, smove, spop, srandmember, srem, sunion, sunionstore, sscan,
                  sscan_iter, set, get)
from .orm import (Key, Set)

__version__ = '0.0.3'
VERSION = tuple(map(int, __version__.split('.')))

__all__ = {'pipeline', 'flushall', 'flushdb', 'connection', 'with_connection', 'with_connect', 'smembers', 'exists',
           'keytype', 'Key', 'Set', 'sismember', 'keys', 'delkey', 'sadd', 'scard', 'sdiff', 'sdiffstore', 'sinter',
           'sinterstore', 'smove', 'spop', 'srandmember', 'srem', 'sunion', 'sunionstore', 'sscan', 'sscan_iter', 'set',
           'get'}

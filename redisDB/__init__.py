from .connect import (connection, with_connection, with_connect)
from .api import (smembers, exists, keytype, sismember, keys, delkey)
from .orm import (Key, Set)

__version__ = '0.0.1'
VERSION = tuple(map(int, __version__.split('.')))

__all__ = ['connection', 'with_connection', 'with_connect', 'smembers', 'exists', 'keytype', 'Key', 'Set'
           "sismember", 'keys', 'delkey']

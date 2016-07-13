from .pool import (create_pool, select_db, close_pool, set_config, set_timeout, have_pool,
                   with_redis, redis_connection)
from .api import rpush

__version__ = '0.0.1'
VERSION = tuple(map(int, __version__.split('.')))

__all__ = ['create_pool', 'select_db', 'close_pool', 'set_config', 'set_timeout', 'rpush', 'have_pool',
           'with_redis', 'redis_connection']

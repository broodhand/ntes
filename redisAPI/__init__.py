from .client import (create_client, select_db, close_client, set_config, set_timeout, have_client, with_redis,
                     redis_client)
from .api import rpush

__version__ = '0.0.3'
VERSION = tuple(map(int, __version__.split('.')))

__all__ = ['create_client', 'select_db', 'close_pool', 'set_config', 'set_timeout', 'rpush', 'have_client',
           'with_redis', 'redis_client']

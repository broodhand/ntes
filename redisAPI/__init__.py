from .redisDB import (connection, with_connection)

__version__ = '0.0.1'
VERSION = tuple(map(int, __version__.split('.')))

__all__ = ['connection', 'with_connection']

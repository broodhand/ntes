from .stock import Base
from .data import get_data
from .url import make_urls


__version__ = '0.2.1'
VERSION = tuple(map(int, __version__.split('.')))

__all__ = ['Base', 'get_data', 'make_urls']



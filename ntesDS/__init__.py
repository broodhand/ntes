from .code import Codes
from .data import get_data
from .url import make_urls


__version__ = '0.2.0'
VERSION = tuple(map(int, __version__.split('.')))

__all__ = ['Codes', 'get_data', 'make_urls']



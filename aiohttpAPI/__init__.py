from .client import (get_urls, get_url)

__version__ = '0.3.1'
VERSION = tuple(map(int, __version__.split('.')))

__all__ = ['get_urls', 'get_url']



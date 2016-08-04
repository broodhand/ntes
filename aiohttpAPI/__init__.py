from .client import (get_urls, get_url, Urls)

__version__ = '0.4.1'
VERSION = tuple(map(int, __version__.split('.')))

__all__ = ['get_urls', 'get_url', 'Urls']

from .client import (get_urls, get_url)
from .api import (Urls, Url)

__version__ = '0.4.2'
VERSION = tuple(map(int, __version__.split('.')))

__all__ = ['get_urls', 'get_url', 'Urls', 'Url']

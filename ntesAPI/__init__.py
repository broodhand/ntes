from .geturls import (get_urls)
from .tools import (make_ntes_url, make_urls, generate_codes, generate_merger_codes, get_all_codes_urls)

__version__ = '0.0.6'
VERSION = tuple(map(int, __version__.split('.')))

__all__ = ['get_urls', 'make_ntes_url', 'make_urls', 'generate_codes', 'generate_merger_codes', 'get_all_codes_urls']



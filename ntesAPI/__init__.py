from .surls import (get_urls)
from .tools import (make_ntes_url, generate_codes, generate_merger_codes)

__version__ = '0.0.4'
VERSION = tuple(map(int, __version__.split('.')))

__all__ = ['get_urls', 'make_ntes_url', 'generate_codes', 'generate_merger_codes']



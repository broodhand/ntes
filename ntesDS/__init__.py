from .code import (of_code_generator, sh_code_generator, sz_code_generator)
from .data import get_data, of_data
from .url import make_urls


__version__ = '0.0.2'
VERSION = tuple(map(int, __version__.split('.')))

__all__ = ['of_code_generator', 'sh_code_generator', 'sz_code_generator', 'of_data', 'get_data', 'make_urls']



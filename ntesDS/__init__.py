from .stock import OF, SH, SZ


__version__ = '0.3.1'
VERSION = tuple(map(int, __version__.split('.')))

__all__ = ['OF', 'SH', 'SZ']



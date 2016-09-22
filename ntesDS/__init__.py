from .stock import OF, OFGeneral, OFCurrency, SH, SHIndex, SZ


__version__ = '0.3.2'
VERSION = tuple(map(int, __version__.split('.')))

__all__ = ['OF', 'OFGeneral', 'OFCurrency', 'SH', 'SHIndex', 'SZ']



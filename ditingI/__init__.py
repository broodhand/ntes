from .tradingdays import init_tradingdays, is_today_trade

__version__ = '0.0.1'
VERSION = tuple(map(int, __version__.split('.')))

__all__ = ['init_tradingdays', 'is_today_trade']

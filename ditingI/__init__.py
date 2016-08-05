from .tradingdays import init_tradingdays, is_trade_day

__version__ = '0.0.2'
VERSION = tuple(map(int, __version__.split('.')))

__all__ = ['init_tradingdays', 'is_trade_day']

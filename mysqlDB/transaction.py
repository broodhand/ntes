import logging; logging.basicConfig(level=logging.INFO)
import functools
import time
from .connect import _db_ctx


def _profiling(start, sql=''):
    t = time.time() - start
    if t > 0.1:
        logging.warning('[PROFILING] [MYSQL] %s: %s' % (t, sql))
    else:
        logging.info('[PROFILING] [MYSQL] %s: %s' % (t, sql))


def with_transaction(func):
    @functools.wraps(func)
    def _wrapper(*args, **kw):
        start = time.time()
        with _transactionctx():
            func(*args, **kw)
        _profiling(start)
    return _wrapper


class _transactionctx(object):
    def __enter__(self):
        global _db_ctx
        self.should_close_conn = False
        if not _db_ctx.is_init():
            _db_ctx.init()
            self.should_close_conn = True
        _db_ctx.transactions += 1
        logging.info('begin transaction...' if _db_ctx.transactions == 1 else 'join current transaction...')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        global _db_ctx
        _db_ctx.transactions -= 1
        try:
            if _db_ctx.transactions == 0:
                if exc_type is None:
                    self.commit()
                else:
                    self.rollback()
        finally:
            if self.should_close_conn:
                _db_ctx.cleanup()

    def commit(self):
        global _db_ctx
        logging.info('commit transaction...')
        try:
            _db_ctx.connection.commit()
            logging.info('commit ok.')
        except:
            logging.warning('commit failed.try rollback...')
            _db_ctx.connection.rollback()
            logging.warning('rollback ok.')
            raise

    def rollback(self):
        global _db_ctx
        logging.warning('rollback transaction...')
        _db_ctx.connection.rollback()
        logging.info('rollback ok.')


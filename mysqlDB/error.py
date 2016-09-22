
class DBError(Exception):
    pass


class MultiColumnsError(DBError):
    pass


class StandardError(Exception):
    pass

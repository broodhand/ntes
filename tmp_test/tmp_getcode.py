
import logging
from datasource import netsds


def getcodemax(codelist):
    import time
    result = dict()
    errorlist = list()
    for index, codes in enumerate(codelist):
        try:
            r = netsds.getncode(*codes)
        except Exception as e:
            logging.info(e)
            errorlist.append(codes)
        else:
            if isinstance(r, dict):
                result.update(r)
            else:
                errorlist.append(codes)
        logging.info('receive data: %s' % r)
        logging.info('running %s / %s ,get %s data' % (index+1, len(codelist), len(result)))
        time.sleep(10)
    return result, errorlist

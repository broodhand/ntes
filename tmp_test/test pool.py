from multiprocessing import Pool
import time


def run(fn, **kwargs):
    print('start %s %s' % (fn, kwargs))
    time.sleep(2)
    print('end %s %s' % (fn, kwargs))
    return fn + 100


if __name__ == '__main__':
    a = {'a': 1}
    t = (x for x in range(100))
    pool = Pool(4)
    result = list()
    for x in t:
        result.append(pool.apply_async(run, (x,), a))
    pool.close()
    pool.join()
    for res in result:
        print(res.get())
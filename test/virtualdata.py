import datasource
import datastructure

ts = datasource.NetsTickData('204001')
cache = datastructure.Cache()
for data in ts.value_generator(1):
    for i in range(1):
        cache.push(data)
    print('dataes:', len(cache.datas))
    print('result:', len(cache.result))
    if len(cache.result)==2:
        for i in range(1):
            print(cache.pop())


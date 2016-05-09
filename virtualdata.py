import datasource
import database

ts = datasource.NetsTickData('204001')
r = database.callback_redis
for data in ts.value_generator():
    r(data)


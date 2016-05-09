import datasource
import database

ts = datasource.NetsTickData('204001')
r = database.rediscallback
for data in ts.value_generator():
    r(data)


from db.mysqldb import mysql_sync

mysql_sync.create_engine_cfgfile('../db/mysql_sync.cfg')
t = dict(name='zhaocheng')
r = mysql_sync.select_one('select * from test', )
print(r.name)

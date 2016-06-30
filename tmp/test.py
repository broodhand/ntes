from db.mysqldb import sync

sync.create_engine_cfgfile('../db/mysql_sync.cfg')
t = dict(name='zhaocheng')
r = sync.select_one('select * from test', )
print(r.name)

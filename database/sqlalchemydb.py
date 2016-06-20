# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 11:02:14 2016

@author:Zhao Cheng
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import configparser


class SqlalchemyDB(object):
    def __init__(self, sqlalchemycfg='sqlalchemydb.cfg'):
        self.sqlalchemycfg = sqlalchemycfg
        config = configparser.ConfigParser()
        with open(self.sqlalchemycfg, 'r') as cfgfile:
            config.read_file(cfgfile)
            self.cfghost = config.get('SQLALCHEMY', 'host')
            self.cfgport = config.get('SQLALCHEMY', 'port')
            self.cfgdatabase = config.get('SQLALCHEMY', 'database')
            self.cfguser = config.get('SQLALCHEMY', 'user')
            self.cfgpassword = config.get('SQLALCHEMY', 'password')
            self.cfgtype = config.get('SQLALCHEMY', 'type')
            self.cfgdriver = config.get('SQLALCHEMY', 'driver')
        self.constr = '%s+%s://%s:%s@%s:%s/%s' % (
            self.cfgtype, self.cfgdriver, self.cfguser, self.cfgpassword, self.cfghost, self.cfgport, self.cfgdatabase)

    # 获取sqlalchemy的session
    def getsession(self):
        engine = create_engine(self.constr)
        Dbsession = sessionmaker(bind=engine)
        return Dbsession()


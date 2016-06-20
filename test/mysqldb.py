# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 11:02:14 2016

@author:Zhao Cheng
"""
import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.ext.declarative

BaseModel = sqlalchemy.ext.declarative.declarative_base()


# 获取sqlalchemy的session
def getsession(constr='mysql+mysqlconnector://spbgcapital:@Tnt7891011@spbgcapital.f3322.net:3306/spbgcapital'):
    from sqlalchemy.orm import sessionmaker
    engine = sqlalchemy.create_engine(constr, echo=True)
    dbsession = sqlalchemy.orm.sessionmaker(bind=engine)
    return dbsession()


# 定义ds_codemap_nets表对象
class Codemap(BaseModel):
    __tablename__ = 'ds_codemap_nets'
    code = sqlalchemy.Column(sqlalchemy.String(20), primary_key=True)
    mappingcode = sqlalchemy.Column(sqlalchemy.String(20))




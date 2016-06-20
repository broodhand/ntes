from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()  # ORM表对象


class Layout(object):
    def __init__(self):
        self.args = ('navigation', 'subnavigation')
        self.packageName = str(__name__).split('.')[-2]
        self.moduleName = str(__name__).split('.')[-1]
        self.ormDict = dict()
        for argName in self.args:
            tableName = '%s_%s_%s' % (self.packageName, self.moduleName, argName)
            attrDict = dict(__tablename__=tableName, seq=Column(Integer, primary_key=True), caption=Column(String(20)),
                            href=Column(String(255)))
            self.ormDict[argName] = type(argName.capitalize(), (Base,), attrDict)

    def get_args_dict(self, sqlalchemysession):
        kw = dict()
        for (arg, obj) in self.ormDict.items():
            kw[arg] = sqlalchemysession.query(obj).order_by('seq').all()
        return kw

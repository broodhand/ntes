from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()  # ORM表对象


class OrmBase(object):
    def __init__(self, args, packagename, modulename, attridict):
        self.args = args
        self.packageName = packagename
        self.moduleName = modulename
        self.attridict = attridict
        self.ormDict = dict()
        for argName in self.args:
            self.attridict['__tablename__'] = '%s_%s_%s' % (self.packageName, self.moduleName, argName)
            ormDict[argName] = type(argName.capitalize(), (Base,), attrdict)
        return ormDict

    def get_args_dict(self, sqlalchemysession, attrdict):
        kw = dict()
        for (arg, obj) in self.get_orm_dict(attrdict).items():
            kw[arg] = sqlalchemysession.query(obj).order_by('seq').all()
        return kw

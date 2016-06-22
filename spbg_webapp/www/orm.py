from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()  # ORM表对象
PROJECTNAME = 'spbg_webapp'


class ViewBase(object):
    def __init__(self, kwlist, viewname):
        self.kwlist = kwlist
        self.project = PROJECTNAME
        self.view = viewname
        self.table = dict()
        for kw in self.kwlist:
            self.table[kw] = '%s_%s_%s' % (self.project, self.view, kw)


class Layout(ViewBase):
    def __init__(self):
        super(Layout, self).__init__(('navigation', 'subnavigation'), 'layout')
        self.orm = dict()
        for kw in self.kwlist:
            attr = dict(__tablename__=self.table[kw],
                        seq=Column(Integer, primary_key=True),
                        caption=Column(String(20)),
                        href=Column(String(255)))
            self.orm[kw] = type(kw.capitalize(), (Base,), attr)

    def get_render_kw(self, sqlalchemysession):
        render = dict()
        for (kw, obj) in self.orm.items():
                render[kw] = sqlalchemysession.query(obj).order_by('seq').all()
        return render


class Home(Layout):
    def __init__(self):
        super(Home, self).__init__()


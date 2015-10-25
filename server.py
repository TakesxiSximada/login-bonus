# -*- coding: utf-8 -*-
import sys
import json
import tornado.ioloop
import tornado.web
from tornado.web import StaticFileHandler

import sqlalchemy as sa
import sqlalchemy.orm as sa_orm
from sqlalchemy.ext.declarative import declarative_base

from zope.interface import Interface  # noqa
from zope.interface.registry import Components
from zope.component.interfaces import IFactory

from zope.sqlalchmey import ZopeTransactionExtension


Base = declarative_base()


class DeviceLog(Base):
    __tablename__ = 'DeviceLog'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    hit = sa.Column(sa.String, default='false')


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")


class DataHandler(tornado.web.RequestHandler):
    def get(self):
        session = create_object([IFactory, 'db-master'])
        session.query(DeviceLog).all()
        data = json.dumps({
            'id': 'DEVICE_ID',
            'count': 5,
            })
        self.write(data)


class UpdateHandler(tornado.web.RequestHandler):
    def post(self):
        data = json.dumps({
            'status': 'success',
            })
        self.write(data)


application = tornado.web.Application([
    (r"/api/update", MainHandler),
    (r"/api/data", DataHandler),
    (r"/(.*)", StaticFileHandler, {'path': './static'}),
])


def create_object(query, *args, **kwds):
    registry = get_registry()
    factory = None

    if isinstance(query, [list, tuple]):
        factory = registry.queryUtility(**query)
    elif isinstance(query, [dict]):
        factory = registry.queryUtility(*query)
    else:
        factory = registry.queryUtility(query)

    if not callable(factory):
        return None

    return factory(*args, **kwds)


def get_registry():
    from zope.component import getGlobalSiteManager
    from zope.interface.interfaces import IComponents
    gsm = getGlobalSiteManager()
    return gsm.queryUtility(IComponents)


def init_registry(registry):
    from zope.component import getGlobalSiteManager
    from zope.interface.interfaces import IComponents
    gsm = getGlobalSiteManager()
    gsm.registerUtility(registry, IComponents)


class SessionFactory(IFactory):
    def __init__(self, sessionmaker):
        self._sessionmaker = sessionmaker

    def __call__(self):
        return sa_orm.scoped_session(self._sessionmaker)


def main(argv=sys.argv[1:]):
    engine = sa.create_engine('sqlite://')
    Session = sa_orm.sessionmaker(bind=engine, extension=ZopeTransactionExtension())
    registry = Components()
    registry.registerUtility(SessionFactory(Session), IFactory, 'db-master')
    init_registry(registry)

    session = create_object([IFactory, 'db-master'])
    session.metadata.create_all(engine)

    application.listen(80)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    sys.exit(main())

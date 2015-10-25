# -*- coding: utf-8 -*-
import sys
import json
import argparse
import tornado.ioloop
import tornado.web
from tornado.web import StaticFileHandler
from sandstorm.handlers import YAStaticFileHandler

import sqlalchemy as sa
import sqlalchemy.orm as sa_orm
from sqlalchemy.ext.declarative import declarative_base

from zope.interface import (
    Interface,  # noqa
    implementer,
    )
from zope.interface.registry import Components
from zope.component.interfaces import IFactory

import transaction
from zope.sqlalchemy import ZopeTransactionExtension


Base = declarative_base()


class DeviceLog(Base):
    __tablename__ = 'DeviceLog'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    code = sa.Column(sa.String)
    hit = sa.Column(sa.String, default='false')


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")


class DataHandler(tornado.web.RequestHandler):
    def get(self):

        device_code = self.request.query_arguments['device_code'][0].decode()
        session = create_object([IFactory, 'db-master'])
        device_logs = session \
            .query(DeviceLog) \
            .filter(DeviceLog.code == device_code) \
            .all()
        data = json.dumps({
            'device_code': device_code,
            'count': len(device_logs),
            })
        self.write(data)


class UpdateHandler(tornado.web.RequestHandler):
    def post(self):
        data = json.loads(self.request.body)
        device_code = data['device_code']
        hit = data['hit']
        device_log = DeviceLog(
            code=device_code,
            hit=hit,
            )
        session = create_object([IFactory, 'db-master'])
        session.add(device_log)
        session.flush()
        transaction.commit()
        data = json.dumps({
            'status': 'success',
            })
        self.write(data)


application = tornado.web.Application([
    (r"/api/update", UpdateHandler),
    (r"/api/data", DataHandler),
    (r"/(.*)", YAStaticFileHandler, {'path': './static'}),
])


def create_object(query, *args, **kwds):
    registry = get_registry()
    factory = None

    if isinstance(query, list) or isinstance(query, tuple):
        factory = registry.queryUtility(*query)
    elif isinstance(query, dict):
        factory = registry.queryUtility(**query)
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


@implementer(IFactory)
class SessionFactory(object):
    def __init__(self, sessionmaker):
        self._sessionmaker = sessionmaker

    def __call__(self):
        return sa_orm.scoped_session(self._sessionmaker)


def main(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', default=80)
    args = parser.parse_args(argv)

    engine = sa.create_engine('sqlite://')
    Session = sa_orm.sessionmaker(bind=engine, extension=ZopeTransactionExtension())
    registry = Components()
    registry.registerUtility(SessionFactory(Session), IFactory, 'db-master')
    init_registry(registry)
    Base.metadata.create_all(engine)

    application.listen(args.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    sys.exit(main())

import json
import tornado.ioloop
import tornado.web
from tornado.web import StaticFileHandler

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")


class DataHandler(tornado.web.RequestHandler):
    def get(self):
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
    (r"/", StaticFileHandler, {'path': './static'}),
])

if __name__ == "__main__":
    application.listen(80)
    tornado.ioloop.IOLoop.current().start()

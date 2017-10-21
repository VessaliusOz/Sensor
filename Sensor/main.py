# encoding:utf8
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Sensor.settings")
from django.core.wsgi import get_wsgi_application
import tornado
import tornado.httpserver
from tornado import web
from tornado.options import define, options
import tornado.wsgi


define("port", default=8080, help="run on the given port", type=int)


def main():

    wsgi_app = tornado.wsgi.WSGIContainer(get_wsgi_application())
    tornado_app = tornado.web.Application([
        (r".*", tornado.web.FallbackHandler, dict(fallback=wsgi_app))
    ])
    http_server = tornado.httpserver.HTTPServer(tornado_app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()


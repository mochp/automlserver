# coding:utf8
import os
import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
import datetime
import time
import functools
from tornado.options import define, options
from concurrent.futures import ThreadPoolExecutor


define("port", type=int, default=5001)


class SyncHandler(tornado.web.RequestHandler):  
    def get(self):     
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        time.sleep(5)
        # os.system("ping -c 2 www.baidu.com")
        self.finish('It works')

class AsyncHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        tornado.ioloop.IOLoop.instance().add_timeout(1, callback=functools.partial(self.ping, 'www.baidu.com'))
        # do something others
        self.finish('It works')

    @tornado.gen.coroutine
    def ping(self, url):
        os.system("ping -c 2 {}".format(url))
        return 'after'

class AsyncTaskHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        # yield 结果
        response = yield tornado.gen.Task(self.ping, ' www.baidu.com')
        # print ('response', response)
        self.finish('hello')

    @tornado.gen.coroutine
    def ping(self, url):
        os.system("ping -c 2 {}".format(url))
        return 'after'



class FutureHandler(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(10)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):

        url = 'www.baidu.com'
        tornado.ioloop.IOLoop.instance().add_callback(functools.partial(self.ping, url))
        self.finish('It works')

    @tornado.concurrent.run_on_executor
    def ping(self, url):
        os.system("ping -c 2 {}".format(url))


class Executor(ThreadPoolExecutor):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not getattr(cls, '_instance', None):
            cls._instance = ThreadPoolExecutor(max_workers=10)
        return cls._instance


class FutureResponseHandler(tornado.web.RequestHandler):
    executor = Executor()

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):

        future = Executor().submit(self.ping, 'www.baidu.com')

        response = yield tornado.gen.with_timeout(datetime.timedelta(10), future,
                                                  quiet_exceptions=tornado.gen.TimeoutError)

        if response:
            print ('response', response.result())

    @tornado.concurrent.run_on_executor
    def ping(self, url):
        os.system("ping -c 1 {}".format(url))
        return 'after'


urls = [
    (r"/sync", SyncHandler),
    (r"/async", AsyncHandler),
    (r"/asynctask", AsyncTaskHandler),
    (r"/asyncfuturetask", FutureResponseHandler),
    (r"/asyncfuture", FutureHandler)
]

base_dir = os.path.dirname(__file__)
configs = dict(
    debug=True,
    template_path=os.path.join(base_dir, "templates"),
)


class CustomApplication(tornado.web.Application):
    def __init__(self, urls, configs):
        handlers = urls
        settings = configs
        super(CustomApplication, self).__init__(handlers=handlers, **settings)


def create_app():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(CustomApplication(urls, configs))
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


app = create_app()

if __name__ == "__main__":
    app()

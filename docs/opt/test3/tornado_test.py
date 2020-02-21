import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.httpclient
import time
import tcelery, tasks
from tornado.options import define, options
tcelery.setup_nonblocking_producer()

define("port", default=8000, help="run on the given port", type=int)

class AsyncMysqlHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self, flag):
        tasks.query_mysql.apply_async(args=[flag], callback=self.on_result)

    def on_result(self, response):
        self.write(response.result)
        self.finish()

class NowHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("i want you, right now!")

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[
            (r"/mysql_query/(\d+)", AsyncMysqlHandler), 
            (r"/i_want_you_now", NowHandler)])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
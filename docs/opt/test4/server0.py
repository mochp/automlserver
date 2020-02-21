import tornado.ioloop
import tornado.web
import tornado
import time
import functools
import os

def handel():
    time.sleep(1)
    return "hello,tornado"

# class MainHandler(tornado.web.RequestHandler):
#     def get(self):
#         res = handel()
#         self.write(res)

class MainHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        tornado.ioloop.IOLoop.instance().add_timeout(1, callback=functools.partial(self.ping, 'www.baidu.com'))
        self.finish('It works')
 

    @tornado.gen.coroutine
    def ping(self, url):
        os.system("ping -c 2 {}".format(url))
        return 'after'

    # @tornado.gen.coroutine
    # def ping(self, url):
    #     time.sleep(1)
    #     # with open("1.txt","a+") as f:
    #     #     f.write(str(time.time())+"\n")
    #     # print("I success!!!")
    #     return 'i receive ' + str(url)

 
def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

def main():
    # app = make_app()
    # app.listen(8000)
    # tornado.ioloop.IOLoop.current().start()
    app = make_app()
    server = tornado.httpserver.HTTPServer(app)
    server.bind(8000)
    server.start(0)  
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()
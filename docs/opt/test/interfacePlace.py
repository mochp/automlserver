# coding:utf8
import os
import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
import json
from lookfor import predict
from jiebapir import pirstring,jiebastring

from tornado.options import define, options

define("port", type=int, default=8091)


class EmotionHandler(tornado.web.RequestHandler):  
    def get(self):     
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

        result = self.get_query_argument('query', 'None')  
        print(result)
        score = 0.11*len(result)
        respon = {"status": 1,
                  "result": score}    
        
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.write(json.dumps(respon))
        self.finish()

class PlaceHandler(tornado.web.RequestHandler):  
    def get(self):         
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        result = self.get_query_argument('query', None)  
        result_tju = predict(result)
        result_cas = ';'.join(pirstring(result))
        result_jb = ';'.join(jiebastring(result))
        print(result_cas,result_jb,result_tju,result)
        respon = {
                "status": 1,
                "result": {
                        "tju": result_tju,
                        "cas": result_cas,
                        "jb": result_jb
                        }
                } 
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.write(json.dumps(respon))
        self.finish()
    
class OpinionHandler(tornado.web.RequestHandler):  

        
    def get(self):     
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        result = self.get_query_argument('query', None)  
        respon = {
                "status": 1,
                "result": {
                            "tju": result,
                            "baidu": {"car": result,
                                      "hotel": result,
                                      "spot": result
                                      }
                            }
                }   
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.write(json.dumps(respon))
        self.finish()  

class ClassificationHandler(tornado.web.RequestHandler):  
    def get(self):   
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        result = self.get_query_argument('query', 'None')  
        score_ad = 0.03*len(result)
        score_sex = 0.013*len(result)
        score_politic = 0.073*len(result)
        score_normal = 0.093*len(result)
        
        respon = {
                "status": 1,
                "result": {
                        "ad": score_ad,
                        "sex": score_sex,
                        "politic": score_politic,
                        "normal": score_normal
                        }
                } 
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.write(json.dumps(respon))
        self.finish()  
 
class CloudHandler(tornado.web.RequestHandler):  
    def get(self):   
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        result = self.get_query_argument('query', 'None')  
        word = result[:2]
        respon = {
                "status": 1,
                "result": [["人工智能",12],["机器学习",10],["自动化",10],
                           ["模式识别",8],["控制工程",6],["大数据",1],
                           ["python",6],["java",2],["c++",2],["c#",4],
                           ["地名抽取",6],["智能化",10],[word,20]]
                }   
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.write(json.dumps(respon))
        self.finish()





urls = [
    (r"/emotion", EmotionHandler),
    (r"/place", PlaceHandler),
    (r"/opinion", OpinionHandler),
    (r"/classification", ClassificationHandler),
    (r"/cloud", CloudHandler)
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

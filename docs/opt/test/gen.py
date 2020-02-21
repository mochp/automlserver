#!/usr/bin/env python
# -*- coding:utf-8 -*-

import tcelery
from tornado.web import RequestHandler
import tornado

tcelery.setup_nonblocking_producer()  # 设置为非阻塞生产者，否则无法获取回调信息


class MyMainHandler(RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        print("begin")
        # 使用yield 获取异步返回值，会一直等待但是不阻塞其他请求
        result = yield tornado.gen.Task(sleep.apply_async, args=[10])
        print("ok - -{}".format(result.result))  # 返回值结果

        # sleep.apply_async((10, ), callback=self.on_success)
        # print("ok -- {}".format(result.get(timeout=100)))#使用回调的方式获取返回值,发送任务之后，请求结束，所以不能放在处理tornado的请求任务当中，因为请求已经结束了，与客户端已经断开连接，无法再在获取返回值的回调中继续向客户端返回数据

        # result = sleep.delay(10)    #delay方法只是对apply_async方法的封装而已
        # data = result.get(timeout=100)  #使用get方法获取返回值，会导致阻塞，相当于同步执行

        def on_success(self, response):  # 回调函数
            print("Ok - - {}".format(response))

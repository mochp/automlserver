#!/usr/bin/env python

# -*-  coding:utf-8 -*-

from tornado.web import Application


from tornado.ioloop import IOLoop


import tcelery

from com.analysis.handlers.data_analysis_handlers import *

from com.analysis.handlers.data_summary_handlers import *

from com.analysis.handlers.data_cid_sumjson_handler import Cid_Sumjson_Handler

from com.analysis.handlers.generator_handlers import GeneratorCsv, GeneratorSpss


Handlers = [

    (r"/single_factor_variance_analysis/(.*)",
     SingleFactorVarianceAnalysis),  # 单因素方差检验

]


if __name__ == "__main__":

    tcelery.setup_nonblocking_producer()

    application = Application(Handlers)

    application.listen(port=8888, address="0.0.0.0")

    IOLoop.instance().start()

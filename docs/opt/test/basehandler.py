#!/usr/bin/env python

# -*-  coding:utf-8 -*-


from collections import defaultdict


import pandas as pd

import numpy as np

import pygal

import tornado.gen

from pygal.style import LightStyle

from tornado.web import RequestHandler

import json


from com.analysis.db.db_engine import DBEngine

from com.analysis.utils.log import LogCF

from com.analysis.handlers.data_cid_sumjson_handler import cid_sumjson


class BaseRequest(RequestHandler):

    def __init__(self, application, request, **kwargs):

        super(BaseRequest, self).__init__(application, request, **kwargs)


class BaseAnalysisRequest(BaseRequest):

    def __init__(self, application, request, **kwargs):

        super(BaseAnalysisRequest, self).__init__(
            application, request, **kwargs)

    @tornado.gen.coroutine
    def celery_task(self, func, params, queue="default_analysis"):

        args_list = list(params)

        args_list.insert(0, "")

        response = yield tornado.gen.Task(func, args=args_list, queue=queue)

        raise tornado.gen.Return(response)



#!/usr/bin/env python

# -*-  coding:utf-8 -*-


import tornado.gen

import tornado.web

from com.analysis.core.base import BaseAnalysisRequest

from com.analysis.tasks.data_analysis import *


class SingleFactorVarianceAnalysis(BaseAnalysisRequest):

    @tornado.gen.coroutine
    def get(self, *args, **kwargs):

        response = yield self.celery_task(single_factor_variance_analysis.apply_async, params=args)

        print(response.result)

        self.write(response.result[2])



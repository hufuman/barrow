#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Jack River'

from django.conf.urls import patterns, include, url
from barrow.views import FetchResultView, IndexView

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'fetch/(?P<application>\w+)', FetchResultView.as_view(), name='fetch-result'),
)
#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Jack River'

from django.conf.urls import patterns, include, url
from barrow.views import *

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'fetch/(?P<application>\w+)/unread', FetchUnreadResultView.as_view(), name='fetch-unread'),
    url(r'fetch/(?P<application>\w+)/time/(?P<timestamp>\w+)', FetchByTimestampView.as_view(), name='fetch-by-time'),
    url(r'reset_spider/$', ResetSpiderView.as_view(), name='reset-spider'),
)
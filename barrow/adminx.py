#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Jack River'

import json
import xadmin

from barrow.models import *


class ApplicationAdmin(object):
    pass


class SpiderAdmin(object):

    def save_models(self):
        self.new_obj.save()

        add_spider_to_scheduler(self.new_obj)


class SpiderTaskAdmin(object):
    list_display = ['spider', 'start_time', 'end_time', 'state']


class SpiderResultAdmin(object):
    pass


xadmin.site.register(Application, ApplicationAdmin)
xadmin.site.register(Spider, SpiderAdmin)
xadmin.site.register(SpiderTask, SpiderTaskAdmin)
xadmin.site.register(SpiderResult, SpiderResultAdmin)

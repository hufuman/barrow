#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Jack River'

import xadmin
import pytz

from barrow.models import *


class ApplicationAdmin(object):
    pass


class SpiderAdmin(object):
    list_display = ['application', 'name', 'running']

    def save_models(self):
        self.new_obj.last_update = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
        self.new_obj.save()


class SpiderTaskAdmin(object):
    list_display = ['spider', 'start_time', 'end_time', 'state']


class SpiderResultAdmin(object):
    list_display = ['hash_value', 'create_time', 'retrieved']


xadmin.site.register(Application, ApplicationAdmin)
xadmin.site.register(Spider, SpiderAdmin)
xadmin.site.register(SpiderTask, SpiderTaskAdmin)
xadmin.site.register(SpiderResult, SpiderResultAdmin)

#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Jack River'

import redis
import os, sys
os.environ['DJANGO_SETTINGS_MODULE'] = 'barrow_devel.settings'
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from django.conf import settings
from barrow.models import SpiderResult


def main():
    r = redis.Redis(**settings.REDIS_CONFIG)
    for result in SpiderResult.objects.all():
        if result.hash_value:
            r.sadd(settings.UNIQUE_SPIDER_RESULT_REDIS_CACHE_NAME, result.hash_value)


if __name__ == '__main__':
    main()
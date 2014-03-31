#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Jack River'

from django.core.management.base import BaseCommand

import json
from barrow.models import Spider, SpiderTask
import pytz

import datetime
import signal
import sys


def signal_handler(signal, frame):
    print 'You pressed Ctrl+C!'
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)


from apscheduler.scheduler import Scheduler

global_schedulers = {}

last_update_time = datetime.datetime(year=1900, month=01, day=01, tzinfo=pytz.utc)


def run_spider_task(spider):
    if spider.running:
        # wait for current spider task to finish
        return
    else:
        SpiderTask.objects.create_and_run(spider)


def add_spider_to_scheduler(spider):
    # manage scheduler
    key = spider.pk
    if key in global_schedulers.keys():
        # spider exists in scheduler list, remove first
        scheduler = global_schedulers.pop(key)
        scheduler.shutdown()

    scheduler = Scheduler()
    cron_config = json.loads(spider.config)['cron']
    minute, hour, day, month, day_of_week = cron_config.split(' ')
    scheduler.add_cron_job(run_spider_task,
                           minute=minute,
                           hour=hour,
                           day=day,
                           month=month,
                           day_of_week=day_of_week,
                           kwargs={'spider': spider})
    scheduler.start()
    global_schedulers[spider.pk] = scheduler


def update_scheduler():
    global last_update_time
    print('start update...')
    try:
        for spider in Spider.objects.filter(running=False):
            print(spider.last_update.strftime('%Y-%m-%d %H:%M:%S'))
            print(last_update_time.strftime('%Y-%m-%d %H:%M:%S'))
            if spider.last_update >= last_update_time:
                add_spider_to_scheduler(spider)
                print('spider %d updated' % spider.pk)
    except Exception, e:
        print(e)

    last_update_time = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)


class Command(BaseCommand):

    def handle(self, *args, **options):
        scheduler = Scheduler()
        scheduler.add_interval_job(update_scheduler, seconds=10)
        scheduler.start()  # g is the greenlet that runs the scheduler loop
        print('Press Ctrl+C to exit')
        while True:
            continue
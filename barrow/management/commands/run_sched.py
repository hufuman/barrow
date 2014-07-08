#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Jack River'

from django.core.management.base import BaseCommand
import threading
import json
from barrow.models import Spider, SpiderTask
import pytz
from django.conf import settings as django_settings
import datetime
from apscheduler.scheduler import Scheduler

global_schedulers = {}
last_update_time = datetime.datetime(year=1900, month=01, day=01, tzinfo=pytz.utc)


def queue_spider_task(spider):
    if spider.running:
        # wait for current spider task to finish
        return
    elif SpiderTask.objects.filter(spider=spider, state=SpiderTask.SPIDER_TASK_STATE.initial).exists():
        # wait while there is any initial task of this spider
        return
    else:
        SpiderTask.objects.create_task(spider)


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
    scheduler.add_cron_job(queue_spider_task,
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


class SpiderTaskRunnerThread(threading.Thread):

    def __init__(self, task):
        self.task = task
        super(SpiderTaskRunnerThread, self).__init__()

    def run(self):
        self.task.run()


_task_runner_available = True


def spider_task_runner():
    """ get spider tasks that are queued for running, and run them
    """
    global _task_runner_available
    if not _task_runner_available:
        # limit to one task runner at the same time
        return
    _task_runner_available = False
    tasks = SpiderTask.objects.filter(state=SpiderTask.SPIDER_TASK_STATE.initial)[:django_settings.CONCURRENT_TASK]
    threads = []
    while tasks.exists():
        for task in tasks:
            new_thread = SpiderTaskRunnerThread(task)
            threads.append(new_thread)
            new_thread.start()
        for thread in threads:
            # wait for all the threads to finish
            thread.join()

        tasks = SpiderTask.objects.filter(state=SpiderTask.SPIDER_TASK_STATE.initial)[:django_settings.CONCURRENT_TASK]

    _task_runner_available = True


class Command(BaseCommand):

    def handle(self, *args, **options):
        scheduler = Scheduler(standalone=True)
        scheduler.add_interval_job(update_scheduler, seconds=10)
        scheduler.add_interval_job(spider_task_runner, seconds=60)  # run spider task runner every minute
        print('Press Ctrl+C to exit')
        try:
            scheduler.start()  # g is the greenlet that runs the scheduler loop
        except (KeyboardInterrupt, SystemExit):
            pass
#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Jack River'

from django.core.management.base import BaseCommand, CommandError
from optparse import make_option

from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from scrapy.utils.project import get_project_settings

from barrow.models import SpiderTask
from barrow.spider import DynamicSpider


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--task_id',
                    dest='task_id',
                    metavar="TASK ID",
                    default='',
                    help='which spider task to run'),
    )

    def handle(self, *args, **options):
        if not options.get('task_id', None):
            raise CommandError('task id must be provided')

        if not SpiderTask.objects.filter(pk=int(options['task_id'])):
            raise CommandError('task not found')

        task = SpiderTask.objects.get(pk=int(options['task_id']))

        spider = DynamicSpider(spider_task=task)
        settings = get_project_settings()
        crawler = Crawler(settings)
        crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
        crawler.configure()
        crawler.crawl(spider)
        crawler.start()
        log.start(loglevel=log.DEBUG, crawler=crawler)
        reactor.run()

        print('done crawling')
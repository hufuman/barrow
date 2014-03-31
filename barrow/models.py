#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Jack River'

import json
import datetime
import hashlib
from fabric.api import local, lcd
from django.conf import settings
from django.db import models
from scrapy.utils.serialize import ScrapyJSONEncoder
from model_utils import Choices


class Application(models.Model):
    """ application model
    """
    name = models.CharField(max_length=255, unique=True, verbose_name=u'Name')
    display_name = models.CharField(max_length=255, verbose_name=u'Display Name')

    class Meta(object):
        app_label = u'barrow'
        verbose_name = u'Application'
        verbose_name_plural = u'Application'

    def __unicode__(self):
        return self.display_name


class Spider(models.Model):
    """ spider model
    """
    application = models.ForeignKey(Application, verbose_name=u'Application')
    name = models.CharField(max_length=255, verbose_name=u'Spider Name', default=u'Default Spider')
    config = models.TextField(verbose_name=u'Spider Config')
    running = models.BooleanField(verbose_name=u'Running', default=False)
    last_update = models.DateTimeField(verbose_name=u'Update Time', auto_now_add=True)

    class Meta(object):
        app_label = u'barrow'
        verbose_name = u'Spider'
        verbose_name_plural = u'Spider'

    def __unicode__(self):
        return self.name


class SpiderTaskManager(models.Manager):
    """ spider task model manager
    """

    def create_and_run(self, spider):
        task = self.create(spider=spider)
        task.run()


class SpiderTask(models.Model):
    """ spider task model
    """
    objects = SpiderTaskManager()

    SPIDER_TASK_STATE = Choices((0, 'initial', u'Initial'),
                                (1, 'running', u'Running'),
                                (2, 'finished', u'Finished'),
                                (3, 'error', u'Error'))

    spider = models.ForeignKey(Spider, verbose_name=u'Spider')
    start_time = models.DateTimeField(auto_now_add=True, verbose_name=u'Start Time')
    end_time = models.DateTimeField(default=None, null=True, blank=True, verbose_name=u'End Time')
    state = models.IntegerField(choices=SPIDER_TASK_STATE, default=SPIDER_TASK_STATE.initial, verbose_name=u'State')

    def run(self):
        """ run task
        """
        self.spider.running = True
        self.spider.save()

        # change to running state
        self.state = self.SPIDER_TASK_STATE.running
        self.save()

        # run scrap from management command
        with lcd(settings.BASE_DIR):
            local('%s manage.py run_scrap --task_id=%d' % (settings.PYTHON_BIN, self.pk))

        # change to finish state
        self.state = self.SPIDER_TASK_STATE.finished
        self.end_time = datetime.datetime.now()
        self.save()

        self.spider.running = False
        self.spider.save()

    class Meta(object):
        app_label = u'barrow'
        verbose_name = u'Spider Task'
        verbose_name_plural = u'Spider Task'


class SpiderResultManager(models.Manager):
    """ spider result model manager
    """

    def add_result(self, spider_task, item, unique=False, unique_keys=None):
        sha = hashlib.sha256()
        sha.update(str(spider_task.spider.pk))  # add spider pk into hash
        json_item = ScrapyJSONEncoder().encode(item)
        if unique:
            for key in unique_keys:
                sha.update(item[key].encode('utf8'))  # hash content by unique keys
            hash_value = sha.hexdigest()

            if self.filter(hash_value=hash_value).exists():
                return None
        else:
            hash_value = sha.update(json_item).hexdigest()  # hash whole content

        return self.create(spider_task=spider_task,
                           hash_value=hash_value,
                           content=json_item)

    # def fetch_result(self, spider_id):
    #     spider = Spider.objects.filter(pk=spider_id)
    #     if not spider.exists():
    #         raise AttributeError('spider not found')
    #     spider = spider[0]
    #
    #     self.filter()  #TODO


class SpiderResult(models.Model):
    """ spider result model
    """
    objects = SpiderResultManager()

    spider_task = models.ForeignKey(SpiderTask, verbose_name=u'Spider Task')
    hash_value = models.CharField(max_length=256, verbose_name=u'Hash')
    content = models.TextField(verbose_name=u'Result Content')
    create_time = models.DateTimeField(verbose_name=u'Create Time', null=True, auto_now_add=True)
    retrieved = models.BooleanField(verbose_name=u'Retrieved', default=False)

    class Meta(object):
        app_label = u'barrow'
        verbose_name = u'Spider Result'
        verbose_name_plural = u'Spider Result'

    def __unicode__(self):
        return self.hash_value
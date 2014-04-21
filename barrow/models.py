#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Jack River'

import multiprocessing
import pytz
import json
import datetime
import hashlib
from fabric.api import local, lcd
from django.utils.translation import ugettext as _
from django.conf import settings
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from scrapy.utils.serialize import ScrapyJSONEncoder
from model_utils import Choices


class Application(models.Model):
    """ application model
    """
    name = models.CharField(max_length=255, unique=True, verbose_name=_(u'Name'))
    display_name = models.CharField(max_length=255, verbose_name=_(u'Display Name'))

    class Meta(object):
        app_label = u'barrow'
        verbose_name = _(u'Application')
        verbose_name_plural = _(u'Application')

    def __unicode__(self):
        return self.display_name


class SpiderTagManager(models.Manager):
    """ spider tag model manager
    """

    def tags_in_application(self, application):
        spiders = Spider.objects.filter(application=application)
        result = set()
        for spider in spiders:
            for tag in spider.tags.all():
                result.add(tag)

        return list(result)


class SpiderTag(models.Model):
    """ spider tag model
    """
    objects = SpiderTagManager()

    name = models.CharField(max_length=255, verbose_name=_(u'Tag Name'))

    class Meta(object):
        app_label = u'barrow'
        verbose_name = _(u'Spider Tag')
        verbose_name_plural = _(u'Spider Tag')

    def __unicode__(self):
        return self.name


class SpiderManager(models.Manager):
    """ spider model manager
    """

    def get_by_tags(self, tag_names):
        tags = list()
        for name in tag_names:
            try:
                SpiderTag.objects.get(name=name)
            except ObjectDoesNotExist:
                pass

        if not tags:
            return None
        else:
            return self.filter(tags__in=tags)

    def reset_spider_state(self):
        self.all().update(running=False)


class Spider(models.Model):
    """ spider model
    """
    objects = SpiderManager()

    SPIDER_PRIORITY_LEVELS = Choices((0, 'unimportant', _(u'Unimportant')),
                                     (1, 'low', _(u'Low')),
                                     (2, 'medium', _(u'Medium')),
                                     (3, 'high', _(u'High')),
                                     (4, 'critical', _(u'Critical')))

    application = models.ForeignKey(Application, verbose_name=_(u'Application'))
    name = models.CharField(max_length=255, verbose_name=_(u'Spider Name'), default=_(u'Default Spider'))
    config = models.TextField(verbose_name=_(u'Spider Config'))
    running = models.BooleanField(verbose_name=_(u'Running'), default=False)
    last_update = models.DateTimeField(verbose_name=_(u'Update Time'), auto_now_add=True)
    tags = models.ManyToManyField(SpiderTag, verbose_name=_(u'Tags'), related_name=u'spiders')
    priority = models.IntegerField(choices=SPIDER_PRIORITY_LEVELS, verbose_name=_(u'Priority'),
                                   default=SPIDER_PRIORITY_LEVELS.low)

    class Meta(object):
        app_label = u'barrow'
        verbose_name = _(u'Spider')
        verbose_name_plural = _(u'Spider')

    def __unicode__(self):
        return self.name


class SpiderTaskManager(models.Manager):
    """ spider task model manager
    """

    def create_task(self, spider):
        self.create(spider=spider)


class TaskRunnerThread(multiprocessing.Process):

    def __init__(self, task):
        self.task = task
        super(TaskRunnerThread, self).__init__()

    def run(self):
        try:
            # run scrap from management command
            with lcd(settings.BASE_DIR):
                local('%s manage.py run_scrap --task_id=%d' % (settings.PYTHON_BIN, self.task.pk))
        except:
            # error occured
            self.task.state = self.task.SPIDER_TASK_STATE.error
            self.task.end_time = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
            self.task.save()


class SpiderTask(models.Model):
    """ spider task model
    """
    objects = SpiderTaskManager()

    SPIDER_TASK_STATE = Choices((0, 'initial', _(u'Initial')),
                                (1, 'running', _(u'Running')),
                                (2, 'finished', _(u'Finished')),
                                (3, 'error', _(u'Error')),
                                (4, 'timeout', _(u'Timeout')),)

    spider = models.ForeignKey(Spider, verbose_name=_(u'Spider'))
    start_time = models.DateTimeField(auto_now_add=True, verbose_name=_(u'Start Time'))
    end_time = models.DateTimeField(default=None, null=True, blank=True, verbose_name=_(u'End Time'))
    state = models.IntegerField(choices=SPIDER_TASK_STATE, default=SPIDER_TASK_STATE.initial, verbose_name=_(u'State'))

    def _run_task(self):
        try:
            # run scrap from management command
            with lcd(settings.BASE_DIR):
                local('%s manage.py run_scrap --task_id=%d' % (settings.PYTHON_BIN, self.pk))
        except:
            # error occured
            self.state = self.task.SPIDER_TASK_STATE.error
            self.end_time = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
            self.save()

    def run(self):
        """ run task
        """
        self.spider.running = True
        self.spider.save()

        # change spider to running state
        self.state = self.SPIDER_TASK_STATE.running
        self.save()

        new_process = multiprocessing.Process(target=self._run_task)
        new_process.start()
        new_process.join(timeout=settings.SPIDER_RUNNER_TIMEOUT)
        if new_process.is_alive():
            # timeout reached, but process is still running, so terminate it, and set task state to TIMEOUT
            new_process.terminate()
            self.state = self.SPIDER_TASK_STATE.timeout
            self.end_time = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
            self.save()
        else:
            if self.state != self.SPIDER_TASK_STATE.error:
                # no error occur while running, so change to finish state
                self.state = self.SPIDER_TASK_STATE.finished
                self.end_time = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
                self.save()

        # change spider to normal state
        self.spider.running = False
        self.spider.save()

    class Meta(object):
        app_label = u'barrow'
        verbose_name = _(u'Spider Task')
        verbose_name_plural = _(u'Spider Task')


class SpiderResultManager(models.Manager):
    """ spider result model manager
    """

    def add_result(self, spider_task, item, unique=False, unique_keys=None, tags=None):
        if not tags:
            tags = []

        sha = hashlib.sha256()
        sha.update(str(spider_task.spider.pk))  # add spider pk into hash
        json_item = ScrapyJSONEncoder().encode(item)
        if unique:
            for key in unique_keys:
                sha.update(item[key].encode('utf8'))  # hash content by unique keys

            # add spider unique
            sha.update('spider' + str(spider_task.spider.pk))

            hash_value = sha.hexdigest()

            if self.filter(hash_value=hash_value).exists():
                return None
        else:
            hash_value = sha.update(json_item).hexdigest()  # hash whole content

        return self.create(spider_task=spider_task,
                           hash_value=hash_value,
                           content=json_item,
                           tags=json.dumps(tags))

    def fetch_result_spider(self, spider):
        results = self.filter(spider_task__spider=spider, retrieved=False)
        if results:
            results.update(retrieved=True)
            return results
        else:
            return []

    def fetch_unread_result_application(self, application):
        results = self.filter(spider_task__spider__application=application, retrieved=False)
        if results.exists():
            return_results = list(results)
            results.update(retrieved=True)
            return return_results
        else:
            return []

    def fetch_result_application_and_time(self, application, request_time):
        results = self.filter(spider_task__spider__application=application, create_time__gt=request_time)
        if results.exists():
            return results
        else:
            return []


class SpiderResult(models.Model):
    """ spider result model
    """
    objects = SpiderResultManager()

    spider_task = models.ForeignKey(SpiderTask, verbose_name=_(u'Spider Task'))
    hash_value = models.CharField(max_length=256, verbose_name=_(u'Hash'))
    content = models.TextField(verbose_name=_(u'Result Content'))
    create_time = models.DateTimeField(verbose_name=_(u'Create Time'), null=True, auto_now_add=True, db_index=True)
    retrieved = models.BooleanField(verbose_name=_(u'Retrieved'), default=False, db_index=True)
    tags = models.TextField(verbose_name=_(u'Tags'), default=u'[]')

    class Meta(object):
        app_label = u'barrow'
        verbose_name = _(u'Spider Result')
        verbose_name_plural = _(u'Spider Result')

    def __unicode__(self):
        return self.hash_value
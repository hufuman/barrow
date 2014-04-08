#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Jack River'

import json
import time
import pytz
from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField, Field
from barrow.models import SpiderResult, SpiderTag


class SpiderResultSerializer(serializers.ModelSerializer):
    """ spider result model serializer
    """
    tags = SerializerMethodField('get_tags')
    create_time = SerializerMethodField('parse_create_time')

    def get_tags(self, instance):
        return json.loads(instance.tags)

    def parse_create_time(self, instance):
        local_tz = pytz.timezone('Asia/Shanghai')
        return time.mktime(instance.create_time.replace(tzinfo=pytz.utc).astimezone(local_tz).timetuple())

    class Meta(object):
        model = SpiderResult
        fields = ['hash_value', 'content', 'create_time', 'tags']


class PrioritizedSpiderResultSerializer(SpiderResultSerializer):
    priority = Field(source='spider_task.spider.priority')

    class Meta(object):
        model = SpiderResult
        fields = ['hash_value', 'content', 'create_time', 'tags', 'priority']


class SpiderTagSerializer(serializers.ModelSerializer):
    """ spider tag model serializer
    """

    class Meta(object):
        model = SpiderTag
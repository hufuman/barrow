#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Jack River'

from rest_framework import serializers
from barrow.models import SpiderResult


class SpiderResultSerializer(serializers.ModelSerializer):
    """ spider result model serializer
    """

    class Meta():
        model = SpiderResult
        fields = ['hash_value', 'content', 'create_time']
#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Jack River'

import datetime
import json
from scrapy.item import Item, Field
from scrapy.spider import Spider, Request
from scrapy.selector import Selector
from django.db.models import get_model


class DynamicItem(Item):
    """ dynamic item
    """

    def __init__(self, item_config):
        self._item_config = item_config
        super(DynamicItem, self).__init__()
        for key in self._item_config.keys():
            self.fields.update({key: Field()})


class DynamicSpider(Spider):
    """ dynamic spider
    """

    def __init__(self, spider_task):
        self.spider_task = spider_task
        self.spider_config = json.loads(self.spider_task.spider.config)
        super(DynamicSpider, self).__init__(name=self.spider_config['application'],
                                            allowed_domains=self.spider_config['allowed_domains'],
                                            start_urls=self.spider_config['start_urls'])

    def _process_strip(self, source, strip_data):
        if isinstance(source, str) or isinstance(source, unicode):
            for strip_key in strip_data:
                if strip_key == '#TAB#':
                    source = source.strip('\t')
                elif strip_key == '#SPACE#':
                    source = source.strip()
                else:
                    source = source.strip(strip_key)

        return source

    def _process_replace(self, source, replace_data):
        if isinstance(source, str) or isinstance(source, unicode):
             for replace_key, replace_value in replace_data.iteritems():
                 source = source.replace(replace_key, replace_value)

        return source

    def parse_item(self, key, field):
        item_config = self.spider_config['item']
        if not key in item_config.keys():
            return field

        key_config = item_config[key]

        # perform parse actions if defined
        if 'parse' in key_config.keys():
            for action in key_config['parse']:
                if action['action'] == 'strip':
                    field = self._process_strip(field, action['data'])
                elif action['action'] == 'replace':
                    field = self._process_replace(field, action['data'])

        # format datetime field type
        if key_config['type'] == 'datetime':
            field = datetime.datetime.strptime(field, key_config['format'])

        return field

    def parse(self, response):
        """ parse first response
        """
        if self.spider_config['url_type'] == 'list_page':
            sel = Selector(response)
            box = sel.xpath(self.spider_config['list_xpath'])
            for x in box:
                item = DynamicItem(self.spider_config['item'])
                for key, value in self.spider_config['xpath']['keys'].iteritems():
                    result = x.xpath(value).extract()
                    if len(result) == 1:
                        # single value
                        item[key] = result[0]
                    else:
                        item[key] = result

                    item[key] = self.parse_item(key, item[key])  # parse item field

                # construct follow request if configured
                if self.spider_config['xpath']['follow'] is not None:
                    # more to follow
                    follow_config = self.spider_config['xpath']['follow']
                    if len(follow_config['follow_info']['url'].keys()) >= 2:
                        # needs string formation
                        arguments = dict()
                        for key, value in follow_config['follow_info']['url'].iteritems():
                            # construct arguments
                            if not key == 'base_url':
                                arguments[key] = item[value]
                        url = follow_config['follow_info']['url']['base_url'].format(**arguments)
                    else:
                        url = follow_config['follow_info']['url']['base_url']

                    request = Request(url, callback=self.parse_follow)
                    request.meta['item'] = item
                    request.meta['config'] = follow_config

                    yield request
                else:
                    # no follow request, so save the item
                    get_model('barrow', 'SpiderResult').objects.add_result(spider_task=self.spider_task,
                                                                           item=item,
                                                                           unique=self.spider_config['unique_result'],
                                                                           unique_keys=self.spider_config[
                                                                               'unique_keys'])

    def parse_follow(self, response):
        """ parse follow response
        """
        follow_config = response.meta.get('config')
        item = response.meta.get('item')

        sel = Selector(response)
        for key, value in follow_config['keys'].iteritems():
            result = sel.xpath(value).extract()
            if len(result) == 1:
                # single value
                item[key] = result[0]
            else:
                item[key] = result

            item[key] = self.parse_item(key, item[key])  # parse item field

        # construct follow request if configured
        if follow_config['follow'] is not None:
            # more to follow
            follow_config = follow_config['follow']
            if len(follow_config['follow_info']['url'].keys()) >= 2:
                # needs string formation
                arguments = dict()
                for key, value in follow_config['follow_info']['url'].iteritems():
                    # construct arguments
                    if not key == 'base_url':
                        arguments[key] = item[value]
                url = follow_config['follow_info']['url']['base_url'].format(**arguments)
            else:
                url = follow_config['follow_info']['url']['base_url']

            request = Request(url, callback=self.parse_follow)
            request.meta['item'] = item
            request.meta['config'] = follow_config

            yield request
        else:
            # no follow request, so save the item
            get_model('barrow', 'SpiderResult').objects.add_result(spider_task=self.spider_task,
                                                                   item=item,
                                                                   unique=self.spider_config['unique_result'],
                                                                   unique_keys=self.spider_config['unique_keys'])
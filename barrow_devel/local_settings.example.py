#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Jack River'

import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = ''

MEDIA_URL = '/media/'
MEDIA_ROOT = ''

PYTHON_BIN = '/Users/jack/Developer/virtualenv/barrow/bin/python'

CONCURRENT_TASK = 3
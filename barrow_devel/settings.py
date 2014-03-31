"""
Django settings for barrow_devel project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

import local_settings


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'n1+&(b#rk-u!+a6=pupxw4df8a4dihi(l9#y&cf5a_&0=$zhn1'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = local_settings.DEBUG

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = local_settings.ALLOWED_HOSTS


# Application definition

EXTERNAL_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'south',
    'xadmin',
    'crispy_forms',
    'reversion',
    'rest_framework',
]

INTERNAL_APPS = [
    'barrow'
]

INSTALLED_APPS = EXTERNAL_APPS + INTERNAL_APPS

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'barrow_devel.urls'

WSGI_APPLICATION = 'barrow_devel.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = local_settings.DATABASES

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = local_settings.STATIC_URL
STATIC_ROOT = local_settings.STATIC_ROOT

MEDIA_URL = local_settings.MEDIA_URL
MEDIA_ROOT = local_settings.MEDIA_ROOT

PYTHON_BIN = local_settings.PYTHON_BIN
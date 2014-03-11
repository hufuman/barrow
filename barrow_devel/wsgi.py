"""
WSGI config for barrow_devel project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "barrow_devel.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from barrow.models import add_spider_to_scheduler, Spider

# add existing spider to global scheduler
for _spider in Spider.objects.all():
    add_spider_to_scheduler(_spider)
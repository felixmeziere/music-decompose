"""
Celery config. Celery is for handling asynch tasks.
"""

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'music_decompose.settings.dev')

APP = Celery('music_decompose')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
APP.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django APP configs.
APP.autodiscover_tasks()


@APP.task(bind=True)
def debug_task(self):
    """
    Self-describing
    """
    print('Request: {0!r}'.format(self.request))

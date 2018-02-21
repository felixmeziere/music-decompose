from __future__ import absolute_import, unicode_literals
from celery import shared_task
import time

@shared_task
def compute_segmentation(x, y):
    time.sleep(10)
    return x + y

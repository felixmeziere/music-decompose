from __future__ import absolute_import, unicode_literals
from celery import shared_task
from segmentation.functions import compute_segmentation

@shared_task
def asynch_compute_segmentation(segment_list_uuid):
    compute_segmentation(segment_list_uuid)


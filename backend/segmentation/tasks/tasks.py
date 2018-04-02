"""
Celery tasks: used to run code asynchronously so that the web app can give immediate feedback
"""
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from segmentation.models import Segmenter
from music_decompose.services import do_task
from .compute_segmentation_for_segmenter import compute_segmentation_for_segmenter

@shared_task
def asynch_compute_segmentation_for_segmenter(segmenter_uuid):
    """
    compute_segmentation in the background
    """
    do_task(
        compute_segmentation_for_segmenter,
        Segmenter,
        segmenter_uuid,
    )

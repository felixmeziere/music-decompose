"""
Celery tasks: used to run code asynchronously so that the web app can give immediate feedback
"""
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .compute_source_separation_for_source_separator import compute_source_separation_for_source_separator

@shared_task
def asynch_compute_source_separation_for_source_separator(song_uuid):
    """
    compute_source_separation_for_source_separator in the background
    """
    compute_source_separation_for_source_separator(song_uuid)

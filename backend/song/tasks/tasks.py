"""
Celery tasks: used to run code asynchronously so that the web app can give immediate feedback
"""
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .compute_tempo_for_song import compute_tempo_for_song

@shared_task
def asynch_compute_tempo_for_song(song_uuid):
    """
    compute_tempo_for_song in the background
    """
    compute_tempo_for_song(song_uuid)

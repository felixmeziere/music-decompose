"""
Celery tasks: used to run code asynchronously so that the web app can give immediate feedback
"""
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from song.models import Song
from music_decompose.services import do_task
from .compute_tempo_for_song import compute_tempo_for_song

@shared_task
def asynch_compute_tempo_for_song(song_uuid):
    """
    compute_tempo_for_song in the background
    """
    do_task(
        compute_tempo_for_song,
        Song,
        song_uuid,
    )

"""
    Defines the song model.
"""
import uuid
from django.db import models


class Song(models.Model):
    """
        Holds meta and file information on a song.
    """
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    added_at = models.DateTimeField(auto_now_add=True)

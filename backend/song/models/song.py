"""
    Defines the song model.
"""
import uuid
from django.db import models


class Song(models.Model):
    """
        Holds meta information on a song and link to files.
    """
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    added_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200)

    def __str__(self):
        return '{0}'.format(self.title)

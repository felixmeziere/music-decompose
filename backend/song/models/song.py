"""
    Defines the Song model.
"""
import uuid
from django.db import models
from song.services import estimate_tempo
import re

class Song(models.Model):
    """
        Holds meta information on a song and link to files.
    """
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    added_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200)
    tempo = models.FloatField(null=True, blank=True)
    sample_rate = models.PositiveIntegerField(blank=True, default=44100)

    def __str__(self):
        return '{0}'.format(self.title)

    def estimate_tempo(self):
        """
        Estimate tempo for this song
        """
        self.tempo = estimate_tempo(self.files.original_file.path)
        self.save()

    @property
    def sanitized_name(self):
        return re.sub(r'[^a-zA-Z0-9]', '', self.title)

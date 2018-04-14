"""
Defines the SourceExtractor model.
"""
from django.db import models
from song.models import Song
from song.sp_functions import compute_tempo
from music_decompose.models import Processor

TEMPO_ESTIMATION_METHOD_CHOICES = (
    ('classic', 'Classic'),
)
PARAMETERS = (
    'method',
)

class TempoEstimator(Processor):
    """
    Contains the computed tempo for a song
    """
    # Class attributes
    parameters = PARAMETERS

    # DB fields
    parent = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='tempo_estimators')
    method = models.CharField(max_length=10, choices=TEMPO_ESTIMATION_METHOD_CHOICES)
    tempo = models.FloatField(null=True, blank=True)

    class Meta:
        """
        Django Meta Class
        """
        unique_together = ('parent',) + PARAMETERS

    def compute_tempo(self):
        """
        Detect tempo of song
        """
        self.tempo = compute_tempo(self.song.original_file.file.name)

    def _process_and_save(self):
        self.compute_tempo()
        self.save()

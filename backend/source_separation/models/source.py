"""
Defines the Source model.
"""
from django.db import models
from django.contrib.postgres.fields import ArrayField
from music_decompose.models import Output

class Source(Output):
    """
    Holds meta information and audio file on a Source
    """
    # DB fields
    parent = models.ForeignKey('source_separation.SourceExtractor', on_delete=models.CASCADE, related_name='sources')
    ind = models.PositiveSmallIntegerField()
    segment_group = ArrayField(models.IntegerField(null=True), null=True)

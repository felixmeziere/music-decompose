"""
Defines the SegmentGroup model.
"""
from django.db import models
from django.contrib.postgres.fields import ArrayField
from music_decompose.models import Output


class SegmentGroup(Output):
    """
    Holds meta information and audio file on a SegmentGroup
    """
    # DB fields
    parent = models.ForeignKey('source_separation.SegmentGrouper', on_delete=models.CASCADE, related_name='segment_groups')
    ind = models.PositiveSmallIntegerField()
    segment_group = ArrayField(models.IntegerField(null=True), null=True)

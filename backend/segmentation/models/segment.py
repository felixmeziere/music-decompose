"""
Defines the Segment model.
"""
from django.db import models
from music_decompose.models import Output


class Segment(Output):
    """
    Holds meta information and audio file on a Segment
    """
    # DB fields
    parent = models.ForeignKey('segmentation.Segmenter', on_delete=models.CASCADE, related_name='segments')
    length_in_samples = models.PositiveIntegerField()
    start_position_in_samples = models.PositiveIntegerField()
    end_position_in_samples = models.PositiveIntegerField()

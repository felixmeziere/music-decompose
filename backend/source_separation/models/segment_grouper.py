"""
Defines the SourceExtractor model.
"""
from django.db import models
from segmentation.models import Segmenter
from music_decompose.models import Processor

SEGMENT_GROUPING_METHOD_CHOICES = (
    ('classic', 'Classic'),
)
PARAMETERS = (
    'method',
)

class SegmentGrouper(Processor):
    """
    Contains the segment groups for a song
    """
    # Class attributes
    data_fields = ('segment_groups',)
    parameters = PARAMETERS

    # DB fields
    parent = models.ForeignKey(Segmenter, on_delete=models.CASCADE, related_name='source_extractors')
    method = models.CharField(max_length=10, choices=SEGMENT_GROUPING_METHOD_CHOICES)

    class Meta:
        """
        Django Meta Class
        """
        unique_together = ('parent',) + PARAMETERS

    @property
    def segmenter(self):
        """
        Convenience field
        """
        return self.parent

"""
Defines the SourceExtractor model.
"""
from django.db import models
from segmentation.models import Segmenter
from music_decompose.models import Processor
from music_decompose.models.make_class import make_processor
from source_separation.sp_functions import group_segments

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
    parent = models.ForeignKey(Segmenter, on_delete=models.CASCADE, related_name='segment_groupers')
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

    def compute_segment_groups(self):
        """
        Given self.segmenter.segment_WFs, compute self.segment_groups containing
        the segment groups
        """
        self.segment_groups = group_segments( # pylint: disable=W0201
            self.method,
            self.segmenter.segment_WFs,
        )

    def process_and_save(self):
        self.compute_segment_groups()
        self.dump_data()
        self.save()

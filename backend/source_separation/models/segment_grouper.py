"""
Defines the SourceExtractor model.
"""
from django.db import models
from segmentation.models import Segmenter
from music_decompose.models import Processor
from music_decompose.sp_services import WFs_to_STFTs
from source_separation.sp_functions import group_segments
from .segment_group import SegmentGroup

PARAMETERS = (
    'method',
    'n_fft',
    'hop_length',
    'win_length',
)
SEGMENT_GROUPING_METHOD_CHOICES = (('classic', 'Classic'), )


class SegmentGrouper(Processor):
    """
    Contains the segment groups for a song
    """
    # Class attributes
    data_fields = ('segment_STFTs', )
    parameters = PARAMETERS

    # DB fields
    parent = models.ForeignKey(Segmenter, on_delete=models.CASCADE, related_name='segment_groupers')
    method = models.CharField(max_length=10, choices=SEGMENT_GROUPING_METHOD_CHOICES)
    n_fft = models.PositiveIntegerField(default=1024)
    hop_length = models.PositiveIntegerField(default=256)
    win_length = models.PositiveIntegerField(default=1024)

    class Meta:
        """
        Django Meta Class
        """
        unique_together = ('parent', ) + PARAMETERS

    @property
    def segmenter(self):
        """
        Convenience field
        """
        return self.parent

    def compute_segment_STFTs(self):
        """
        Get and store segment STFTs from segment WFs
        """
        self.segment_STFTs = WFs_to_STFTs(    # pylint: disable=W0201
            self.segmenter.segment_WFs,
            self.n_fft,
            self.hop_length,
            self.win_length,
        )

    def compute_segment_groups(self):
        """
        Given self.segmenter.segment_WFs, compute self.segment_groups containing
        the segment groups
        """
        segment_groups = group_segments(    # pylint: disable=W0201
            self.method,
            self.segmenter.segment_WFs,
        )
        SegmentGroup.objects.bulk_create([SegmentGroup(parent=self, ind=i, segment_group=segment_group) for i, segment_group in enumerate(segment_groups)])

    def _process_and_save(self):
        self.compute_segment_STFTs()
        self.compute_segment_groups()
        self.dump_data()
        self.save()

    @property
    def segment_groups_list(self):
        """
        Segment groups as a list of lists
        """
        return [segment_group.segment_group for segment_group in self.segment_groups.order_by('ind')]

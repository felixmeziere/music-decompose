"""
Defines the SourceExtractor model.
"""
import uuid
from django.db import models
from segmentation.models import Segmenter
from music_decompose.services import load_fields_from_hdf5, save_fields_to_hdf5
from music_decompose.constants import STATUS_CHOICES

SEGMENT_GROUPING_METHOD_CHOICES = (
    ('classic', 'Classic'),
)

class SegmentGrouper(models.Model):
    """
    Contains the segment groups for a song
    """
    # DB fields
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    added_at = models.DateTimeField(auto_now_add=True)
    segmenter = models.ForeignKey(Segmenter, on_delete=models.CASCADE, related_name='source_extractors')
    method = models.CharField(max_length=10, choices=SEGMENT_GROUPING_METHOD_CHOICES)
    segment_grouping_status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='not_started')

    def __str__(self):
        return 'Segment Grouper for Song: {0} - {1} method'.format(str(self.song), self.method)

    class Meta:
        """
        Django Meta class
        """
        unique_together = ('segmenter', 'method')

    def __init__(self, *args, segment_groups=None, **kwargs):
        super(SegmentGrouper, self).__init__(*args, **kwargs)
        self._segment_groups = segment_groups

    @property
    def song(self):
        """
        Song instance attached to this
        """
        return self.segmenter.song

    @property
    def data_path(self):
        """
        HDF5 file containing heavy data
        """
        return '{0}/segment_grouper_{1}.hdf5'.format(self.absolute_folder_name, self.uuid)

    @property
    def param_string(self):
        """
        Name containing parameters suitable for paths
        """
        return '{0}'.format(self.method)

    @property
    def media_folder_name(self):
        """
        Folder where all this Segment Grouper's-related files will be.
        Relative path from /media
        """
        return '{0}/source_separation/{1}_{2}'.format(self.song.sanitized_name, self.segmenter.param_string, self.param_string)

    @property
    def absolute_folder_name(self):
        """
        Folder where all this Segment Grouper's-related files will be.
        Absolute path from root of project
        """
        return 'music_decompose/media/{0}'.format(self.media_folder_name)

    @property
    def segment_groups(self):
        """
        Array containing the segment groups as rows.
        A segment group contains the indices of the segments used
        to get a given source
        """
        if self._segment_groups is None:
            load_fields_from_hdf5(self, ['segment_groups'])

        return self._segment_groups

    def dump_data(self):
        """
        Dump instance data to disk
        """
        fields = (
            'segment_groups',
        )
        save_fields_to_hdf5(self, fields)

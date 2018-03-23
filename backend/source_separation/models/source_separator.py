"""
Defines the SourceSeparator model.
"""
import uuid
from django.db import models
from segmentation.models import Segmenter
from music_decompose.services import load_fields_from_hdf5, save_fields_to_hdf5
from music_decompose.constants import STATUS_CHOICES

SOURCE_SEPARATION_METHOD_CHOICES = (
    ('classic', 'Classic'),
)

class SourceSeparator(models.Model):
    """
    Contains all the sources for a song and specific methods to handle them
    """
    # DB fields
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    added_at = models.DateTimeField(auto_now_add=True)
    segmenter = models.ForeignKey(Segmenter, on_delete=models.CASCADE, related_name='source_separators')
    method = models.CharField(max_length=10, choices=SOURCE_SEPARATION_METHOD_CHOICES)
    source_separation_status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='not_started')
    data_path = models.CharField(max_length=500, null=True)

    def __str__(self):
        return 'Source Separator for Song: {0} - {1} method'.format(str(self.segmenter.song), self.method)

    class Meta:
        """
        Django Meta class
        """
        unique_together = ('segmenter', 'method')

    def __init__(self, *args, segment_groups=None, source_WFs=None, **kwargs):
        super(SourceSeparator, self).__init__(*args, **kwargs)
        self._segment_groups = segment_groups
        self._source_WFs = source_WFs
        if not self.data_path:
            self.data_path = '{0}/source_separator_{1}.hdf5'.format(self.absolute_folder_name, self.uuid)

    @property
    def param_string(self):
        """
        Name containing parameters suitable for paths
        """
        return '{0}'.format(self.method)

    @property
    def media_folder_name(self):
        """
        Folder where all this Source Separators'-related files will be.
        Relative path from /media
        """
        return '{0}/source_separation/{1}_{2}'.format(self.segmenter.song.sanitized_name, self.segmenter.param_string, self.param_string)

    @property
    def absolute_folder_name(self):
        """
        Folder where all this Source Separators'-related files will be.
        Absolute path from root of project
        """
        return 'music_decompose/media/{0}'.format(self.media_folder_name)

    @property
    def segment_groups(self):
        """
        Array containing the segment groups as rows.
        A segment group contains the indices of the segments used
        to get a given source.
        """
        if self._segment_groups is None:
            load_fields_from_hdf5(self, ['segment_groups'])

        return self._segment_groups

    @property
    def source_WFs(self):
        """
        Array with the waveforms of the sources as rows.
        """
        if self._source_WFs is None and self.data_path is not None:
            load_fields_from_hdf5(self, ['source_WFs'])

        return self._segment_WFs

    def dump_data(self):
        """
        Dump instance data to disk
        """
        fields = (
            'segment_groups',
            'source_WFs',
        )
        save_fields_to_hdf5(self, fields)

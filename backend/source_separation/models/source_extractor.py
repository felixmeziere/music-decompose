"""
Defines the SourceExtractor model.
"""
import uuid
from django.db import models
import numpy as np
from music_decompose.services import load_fields_from_hdf5, save_fields_to_hdf5
from music_decompose.constants import STATUS_CHOICES
from .segment_grouper import SegmentGrouper
from .source import Source

SOURCE_SEPARATION_METHOD_CHOICES = (
    ('classic', 'Classic'),
)

class SourceExtractor(models.Model):
    """
    Contains all the sources for a song and specific methods to handle them
    """
    # DB fields
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    added_at = models.DateTimeField(auto_now_add=True)
    segment_grouper = models.ForeignKey(SegmentGrouper, on_delete=models.CASCADE, related_name='source_extractors')
    method = models.CharField(max_length=10, choices=SOURCE_SEPARATION_METHOD_CHOICES)
    source_separation_status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='not_started')

    def __str__(self):
        return 'Source Extractor for Song: {0} - {1} method'.format(str(self.song), self.method)

    class Meta:
        """
        Django Meta class
        """
        unique_together = ('segment_grouper', 'method')

    def __init__(self, *args, source_WFs=None, **kwargs):
        super(SourceExtractor, self).__init__(*args, **kwargs)
        self._source_WFs = source_WFs

    @property
    def segmenter(self):
        """
        Segmenter instance attached to this
        """
        return self.segment_grouper.segmenter

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
        return '{0}/source_extractor_{1}.hdf5'.format(self.absolute_folder_name, self.uuid)

    @property
    def param_string(self):
        """
        Name containing parameters suitable for paths
        """
        return '{0}'.format(self.method)

    @property
    def media_folder_name(self):
        """
        Folder where all this Source Extractor's-related files will be.
        Relative path from /media
        """
        return '{0}/source_separation/{1}_{2}_{3}'.format(
            self.song.sanitized_name,
            self.segmenter.param_string,
            self.segment_grouper.param_string,
            self.param_string,
        )

    @property
    def absolute_folder_name(self):
        """
        Folder where all this Source Extractor's-related files will be.
        Absolute path from root of project
        """
        return 'music_decompose/media/{0}'.format(self.media_folder_name)

    @property
    def source_WFs(self):
        """
        Array with the waveforms of the sources as rows
        """
        if self._source_WFs is None and self.data_path is not None:
            load_fields_from_hdf5(self, ['source_WFs'])

        return self._source_WFs

    def dump_data(self):
        """
        Dump instance data to disk
        """
        fields = (
            'source_WFs',
        )
        save_fields_to_hdf5(self, fields)

    def create_source_WFs(self):
        """
        Given self.segment_grouper.segment_groups, create self.source_WFs containing
        as rows the waveform of every source
        """
        self._source_WFs = np.zeros((self.segment_grouper.segment_groups.shape[0], len(self.song.song_WF)))
        for i, _ in enumerate(self.segment_grouper.segment_groups):
            self._source_WFs[i, :] = self.song.song_WF

    def create_sources(self):
        """
        Given self.source_WFs, create source entries in the db and their corresponding audio files
        """
        self.sources.all().delete()
        sources = []
        for i, source_WF in enumerate(self.source_WFs):
            source = Source(
                source_index=i,
                source_extractor=self,
                segment_group=list(self.segment_grouper.segment_groups[i]),
                source_WF=source_WF,
            )
            source.write_audio_file()
            sources.append(source)
        Source.objects.bulk_create(sources)

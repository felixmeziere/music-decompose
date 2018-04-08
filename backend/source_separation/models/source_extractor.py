"""
Defines the SourceExtractor model.
"""
from django.db import models
import numpy as np
from music_decompose.models import Processor
from source_separation.models.segment_grouper import SegmentGrouper
from source_separation.models.source import Source
from source_separation.sp_functions import extract_sources_from_segment_groups

SOURCE_SEPARATION_METHOD_CHOICES = (
    ('classic', 'Classic'),
)

PARAMETERS = (
    'method',
)
class SourceExtractor(Processor):
    """
    Contains all the sources for a song and specific methods to handle them
    """
    # Class attributes
    data_fields = ('source_WFs',)
    parameters = PARAMETERS

    # DB fields
    parent = models.ForeignKey(SegmentGrouper, on_delete=models.CASCADE, related_name='source_extractors')
    method = models.CharField(max_length=10, choices=SOURCE_SEPARATION_METHOD_CHOICES)

    class Meta:
        """
        Django Meta Class
        """
        unique_together = ('parent',) + PARAMETERS

    @property
    def segment_grouper(self):
        """
        Convenience field
        """
        return self.parent

    def compute_source_WFs(self):
        """
        Given self.segment_grouper.segment_groups, compute self.source_WFs containing
        as rows the waveform of every source
        """
        _, self.source_WFs = extract_sources_from_segment_groups( # pylint: disable=W0201
            self.method,
            self.segment_grouper.segment_groups,
            self.segment_grouper.segmenter.segment_WFs,
        )

    def create_sources(self):
        """
        Given self.source_WFs, create source entries in the db and their corresponding audio files
        """
        self.sources.all().delete()
        sources = []
        for i, source_WF in enumerate(self.source_WFs):
            source = Source(
                ind=i,
                parent=self,
                segment_group=list(self.segment_grouper.segment_groups[i]),
                WF=source_WF,
            )
            source.write_audio_file()
            sources.append(source)
        Source.objects.bulk_create(sources)

    def process_and_save(self):
        self.compute_source_WFs()
        self.create_sources()
        self.dump_data()
        self.save()

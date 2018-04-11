"""
Defines the Segmenter model.
"""
import numpy as np
from django.db import models
from song.models import TempoEstimator
from segmentation.models import Segment
from segmentation.sp_functions import compute_segmentation
from music_decompose.models import Processor

SEGMENTATION_METHOD_CHOICES = (
    ('blind', 'Blind'),
    ('flexible', 'Flexible'),
)
PARAMETERS = (
    'method',
    'n_tempo_lags_per_segment',
)

class Segmenter(Processor):
    """
    Contains all the segments for a song and specific methods to handle them
    """
    # Class attributes
    data_fields = ('segment_starts_IS', 'segment_WFs')
    parameters = PARAMETERS

    # DB fields
    parent = models.ForeignKey(TempoEstimator, on_delete=models.CASCADE, related_name='segmenters')
    method = models.CharField(max_length=10, choices=SEGMENTATION_METHOD_CHOICES)
    n_tempo_lags_per_segment = models.PositiveSmallIntegerField(default=4)

    class Meta:
        """
        Django Meta Class
        """
        unique_together = ('parent', 'method', 'n_tempo_lags_per_segment',)

    def compute_segment_starts_IS(self):
        """
        Detect segment limits
        """
        self.segment_starts_IS = compute_segmentation( # pylint: disable=W0201
            self.method,
            self.song.song_WF,
            self.song.sample_rate,
            self.parent.tempo,
            self.n_tempo_lags_per_segment,
        )

    def compute_segment_WFs(self):
        """
        Given self.segment_starts_IS, create self.segment_WFs containing
        as rows the waveform of every segment
        """
        n_segments = len(self.segment_starts_IS)
        segment_length = self.segment_starts_IS[1] - self.segment_starts_IS[0]
        self.segment_WFs = np.zeros((n_segments, segment_length)) # pylint: disable=W0201
        for i in range(n_segments-1):
            start = self.segment_starts_IS[i]
            end = self.segment_starts_IS[i+1]
            self.segment_WFs[i, :end - start] = self.song.song_WF[start:end]

    def create_segments(self):
        """
        Given self.segment_WFs, create segment entries in the db and their corresponding audio files
        """
        self.segments.all().delete()
        segments = []
        for i, segment_WF in enumerate(self.segment_WFs):
            segment = Segment(
                ind=i,
                parent=self,
                length_in_samples=len(segment_WF),
                start_position_in_samples=self.segment_starts_IS[i],
                end_position_in_samples=self.segment_starts_IS[i+1] if i < len(self.segment_WFs) - 1 else self.segment_starts_IS[i] + len(segment_WF),
                WF=segment_WF,
            )
            segment.write_audio_file()
            segments.append(segment)
        Segment.objects.bulk_create(segments)

    def process_and_save(self):
        self.compute_segment_starts_IS()
        self.compute_segment_WFs()
        self.create_segments()
        self.dump_data()
        self.save()

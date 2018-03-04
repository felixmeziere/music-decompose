"""
Defines the Segmenter model.
"""
import uuid
import numpy as np
from django.db import models
from song.models import Song
from segmentation.models import Segment
from music_decompose.services import load_fields_from_hdf5, save_fields_to_hdf5
from music_decompose.constants import STATUS_CHOICES

SEGMENTATION_METHOD_CHOICES = (
    ('blind', 'Blind'),
    ('flexible', 'Flexible'),
)

def get_upload_path(instance, _):
    """
    Get path to upload files to. Changes with the song.
    """
    return instance.media_folder_name

class Segmenter(models.Model):
    """
    Contains all the segments for a song and specific methods to handle them
    """
    # DB fields
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    added_at = models.DateTimeField(auto_now_add=True)
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='segmenters')
    method = models.CharField(max_length=10, choices=SEGMENTATION_METHOD_CHOICES)
    tempo = models.FloatField()
    n_tempo_lags_per_segment = models.PositiveSmallIntegerField(default=4)
    segmentation_status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='not_started')
    data_path = models.CharField(max_length=500, null=True)

    def __str__(self):
        return 'Segmenter for Song: {0} - {1} method'.format(str(self.song), self.method)

    class Meta:
        """
        Django Meta class
        """
        unique_together = ('song', 'method', 'n_tempo_lags_per_segment')

    def __init__(self, *args, segment_starts_IS=None, segment_WFs=None, **kwargs):
        super(Segmenter, self).__init__(*args, **kwargs)
        self._segment_starts_IS = segment_starts_IS
        self._segment_WFs = segment_WFs
        if not self.data_path:
            self.data_path = '{0}/segmenter_{1}.hdf5'.format(self.absolute_folder_name, self.song.sanitized_name)

    @property
    def media_folder_name(self):
        """
        Folder where all this segmentLists'-related files will be
        Relative path from /media
        """
        return '{0}/segmentation/{1}'.format(self.song.sanitized_name, self.method)

    @property
    def absolute_folder_name(self):
        """
        Folder where all this segmentLists'-related files will be
        Absolute path from root of project
        """
        return 'music_decompose/media/{0}'.format(self.media_folder_name)


    @property
    def segment_starts_IS(self):
        """
        Array with the positions of the segments starts.
        """
        if self._segment_starts_IS is None:
            load_fields_from_hdf5(self, ['segment_starts_IS'])

        return self._segment_starts_IS

    @property
    def segment_WFs(self):
        """
        Array with the waveforms of the segments as rows.
        """
        if self._segment_WFs is None and self.data_path is not None:
            load_fields_from_hdf5(self, ['segment_WFs'])

        return self._segment_WFs

    def dump_data(self):
        """
        Dump instance data to disk
        """
        fields = (
            'segment_starts_IS',
            'segment_WFs',
        )
        save_fields_to_hdf5(self, fields)

    def create_segment_WFs(self):
        """
        Given self.segment_starts_IS, create self.segment_WFs containing
        as rows the waveform of every segment
        """
        if self.segment_starts_IS is not None:
            n_segments = len(self.segment_starts_IS)
            segment_length = self.segment_starts_IS[1] - self.segment_starts_IS[0]
            self._segment_WFs = np.zeros((n_segments, segment_length))
            for i in range(n_segments-1):
                start = self.segment_starts_IS[i]
                end = self.segment_starts_IS[i+1]
                self._segment_WFs[i, :end - start] = self.song.song_WF[start:end]

    def create_segments(self):
        """
        Given self.segment_WFs, create segment entries in the db and their corresponding audio files
        """
        if self.segment_WFs is not None and self.segment_starts_IS is not None:
            self.segments.all().delete()
            segments = []
            for i, segment_WF in enumerate(self.segment_WFs):
                segment = Segment(
                    segment_index=i,
                    segmenter=self,
                    length_in_samples=len(segment_WF),
                    start_position_in_samples=self.segment_starts_IS[i],
                    end_position_in_samples=self.segment_starts_IS[i+1] if i < len(self.segment_WFs) - 1 else self.segment_starts_IS[i] + len(segment_WF),
                    segment_WF=segment_WF,
                )
                segment.write_audio_file()
                segments.append(segment)
            Segment.objects.bulk_create(segments)

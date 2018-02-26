"""
    Defines the SegmentList model.
"""
import uuid
from django.db import models
from song.models import Song
from segmentation.models import Segment
import numpy as np
import soundfile as sf
import os
import h5py
import librosa as lr

SEGMENTATION_METHOD_CHOICES = (
    ('blind', 'Blind'),
    ('flexible', 'Flexible'),
)

SEGMENTATION_STATUS_CHOICES = (
    ('not_started', 'Not started'),
    ('pending', 'Pending...'),
    ('failed', 'Failed'),
    ('done', 'Done'),
)

def get_upload_path(instance, _):
    return instance.folder_name

class SegmentList(models.Model):
    """
        Contains all the segments for a song and specific methods to handle them
    """
    # DB fields
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    added_at = models.DateTimeField(auto_now_add=True)
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='segment_lists')
    method = models.CharField(max_length=10, choices=SEGMENTATION_METHOD_CHOICES)
    n_tempo_lags_per_segment = models.PositiveSmallIntegerField(default=8)
    segmentation_status = models.CharField(max_length=15, choices=SEGMENTATION_STATUS_CHOICES, default='not_started')
    data_path = models.CharField(max_length=500, null=True)

    def __str__(self):
        return 'Segment List for Song: {0} - {1} method'.format(str(self.song), self.method)

    class Meta:
        """
        Django Meta class
        """
        unique_together = ('song', 'method', 'n_tempo_lags_per_segment')

    def __init__(self, *args, segment_starts_IS=None, segment_WFs=None, **kwargs):
        super(SegmentList, self).__init__(*args, **kwargs)
        self.segment_starts_IS = segment_starts_IS
        self.segment_WFs = segment_WFs


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

    def dump_data(self):
        """
        Dump instance data to disk and save reference in instance
        """
        with h5py.File('{0}/segmentation_{1}.hdf5'.format(self.absolute_folder_name, self.song.sanitized_name), 'w') as data_file:
            data_file.create_dataset('segment_starts_IS', (len(self.segment_starts_IS),), dtype='i', data=self.segment_starts_IS)
            data_file.create_dataset('segment_WFs', (len(self.segment_WFs), len(self.segment_WFs[0])), dtype='f', data=np.array(self.segment_WFs))
            self.data_path = data_file.filename

    def load_data(self):
        """
        Load instance data from disk
        """
        with h5py.File(self.data_path, 'r') as data_file:
            self.segment_starts_IS = data_file['segment_starts_IS'][()]
            self.segment_WFs = data_file['segment_WFs'][()]

    def create_segment_WFs(self, song_WF=None):
        if self.segment_starts_IS is not None:
            if song_WF is not None:
                song_WF, _ = self.song.WF
            n_segments = len(self.segment_starts_IS)
            segment_length = self.segment_starts_IS[1] - self.segment_starts_IS[0]
            self.segment_WFs = np.zeros((n_segments, segment_length))
            for i in range(n_segments-1):
                start = self.segment_starts_IS[i]
                end = self.segment_starts_IS[i+1]
                self.segment_WFs[i, :end - start] = song_WF[start:end]

    def create_segments(self):
        if self.segment_WFs is not None and self.segment_starts_IS is not None:
            self.segments.all().delete()
            segments = []
            for i, segment_WF in enumerate(self.segment_WFs):
                segment = Segment(
                    segment_index=i,
                    segment_list=self,
                    length_in_samples=len(segment_WF),
                    start_position_in_samples=self.segment_starts_IS[i],
                    end_position_in_samples=self.segment_starts_IS[i+1] if i < len(self.segment_WFs) - 1 else self.segment_starts_IS[i] + len(segment_WF),
                    WF=segment_WF,
                )
                segment.write_audio_file()
                segments.append(segment)
            Segment.objects.bulk_create(segments)


"""
    Defines the Segment model.
"""
import uuid
import os
from django.db import models
from music_decompose.services import rank_4_audacity, write_WF
from django.conf import settings
from django.db.models.signals import pre_delete, pre_save

class Segment(models.Model):
    """
        Holds meta information and audio file on a Segment
    """
    # DB fields
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    added_at = models.DateTimeField(auto_now_add=True)
    segment_index = models.PositiveIntegerField()
    segment_list = models.ForeignKey('segmentation.SegmentList', on_delete=models.CASCADE, related_name='segments')
    length_in_samples = models.PositiveIntegerField()
    start_position_in_samples = models.PositiveIntegerField()
    end_position_in_samples = models.PositiveIntegerField()
    audio_file = models.FileField(null=True, blank=True)

    def __str__(self):
        return 'Segment {0} of Song {1} with method {2}'.format(self.segment_index, str(self.segment_list.song), self.segment_list.method)

    class Meta:
        unique_together = ('segment_index', 'segment_list',)

    def __init__(self, *args, WF=None, **kwargs):
        super(Segment, self).__init__(*args, **kwargs)
        self.WF = WF


    @property
    def media_folder_name(self):
        """
        Folder where all this segment's-related files will be
        Relative path from /medias
        """
        return '{0}/segments'.format(self.segment_list.media_folder_name)

    @property
    def absolute_folder_name(self):
        """
        Folder where all this segment's-related files will be
        Absolute path from root of project
        """
        return '{0}/segments'.format(self.segment_list.absolute_folder_name)

    def write_audio_file(self):
        """
        Create or overwrite audio file and attach to instance
        """
        if self.WF is not None:
            file_name = '{0}.{1}'.format(rank_4_audacity(self.segment_index), 'wav')
            write_WF(self.WF, '{0}/{1}'.format(self.absolute_folder_name, file_name), self.segment_list.song.sample_rate)
            self.audio_file = '{0}/{1}'.format(self.media_folder_name, file_name)
        else:
            raise ValueError('Create Audio File was called but there is no WF for segment {0}'.format(str(self)))

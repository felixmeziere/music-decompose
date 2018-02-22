"""
    Defines the SegmentList model.
"""
import uuid
from django.db import models
from song.models import Song
import numpy as np

SEGMENTATION_METHOD_CHOICES = (
    ('blind', 'Blind'),
    ('flexible', 'Flexible'),
)

SEGMENTATION_STATUS_CHOICES = (
    ('not_started', 'Not started'),
    ('pending', 'Pending...'),
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
    segmentation_status = models.CharField(max_length=15, choices=SEGMENTATION_STATUS_CHOICES, default='not_started')
    data_path = models.CharField(max_length=500, null=True)

    def __str__(self):
        return 'Segment List for Song: {0} with {1} method'.format(str(self.song), self.method)

    class Meta:
        """
        Django Meta class
        """
        unique_together = ('song', 'method',)

    @property
    def folder_name(self):
        """
        Folder where all this segmentLists'-related files will be
        """
        return '{0}/segmentation/{1}'.format(self.song.sanitized_name, self.method)


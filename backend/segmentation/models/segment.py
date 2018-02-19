"""
    Defines the Segment model.
"""
import uuid
from django.db import models
from segmentation.models.segment_list import SegmentList

class Segment(models.Model):
    """
        Holds meta information and audio file on a Segment
    """
    # DB fields
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    added_at = models.DateTimeField(auto_now_add=True)
    index = models.PositiveIntegerField()
    segment_list = models.ForeignKey(SegmentList, on_delete=models.CASCADE, related_name='segments')
    length_in_samples = models.PositiveIntegerField()
    start_position_in_samples = models.PositiveIntegerField()
    end_position_in_samples = models.PositiveIntegerField()
    audio_file = models.FileField(null=True)

    def __str__(self):
        return 'Segment {0} of Song {1} with method {2}'.format(self.index, str(self.segment_list.song), self.segment_list.method)

    class Meta:
        unique_together = ('index', 'segment_list',)
# segments = []
# for index in range(30):
#     segments.append(
#         Segment(
#             index=index,
#             segment_list=sl,
#             length_in_samples=3000,
#             start_position_in_song=3000 * index,
#             end_position_in_song=3000 * (index + 1),
#         )
#     )

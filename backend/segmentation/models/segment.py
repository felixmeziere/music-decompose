"""
Defines the Segment model.
"""
import uuid
from django.db import models
from audiofield.fields import AudioField
from music_decompose.services import rank_4_audacity, write_WF
class Segment(models.Model):
    """
        Holds meta information and audio file on a Segment
    """
    # DB fields
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    added_at = models.DateTimeField(auto_now_add=True)
    segment_index = models.PositiveIntegerField()
    segmenter = models.ForeignKey('segmentation.Segmenter', on_delete=models.CASCADE, related_name='segments')
    length_in_samples = models.PositiveIntegerField()
    start_position_in_samples = models.PositiveIntegerField()
    end_position_in_samples = models.PositiveIntegerField()
    audio_file = AudioField(blank=True, ext_whitelist=('.wav'), help_text=('Allowed type: .wav'))

    def __str__(self):
        return 'Segment {0} of Song {1}'.format(self.segment_index, str(self.segmenter.song)) #pylint: disable=E1101

    class Meta:
        unique_together = ('segment_index', 'segmenter',)

    def __init__(self, *args, segment_WF=None, **kwargs):
        super(Segment, self).__init__(*args, **kwargs)
        self.segment_WF = segment_WF


    @property
    def media_folder_name(self):
        """
        Folder where all this segment's-related files will be
        Relative path from /medias
        """
        return '{0}/segments'.format(self.segmenter.media_folder_name) #pylint: disable=E1101

    @property
    def absolute_folder_name(self):
        """
        Folder where all this segment's-related files will be
        Absolute path from root of project
        """
        return '{0}/segments'.format(self.segmenter.absolute_folder_name) #pylint: disable=E1101

    def write_audio_file(self):
        """
        Create or overwrite audio file and attach to instance
        """
        if self.segment_WF is not None:
            file_name = '{0}.{1}'.format(rank_4_audacity(self.segment_index), 'wav')
            write_WF(self.segment_WF, '{0}/{1}'.format(self.absolute_folder_name, file_name), self.segmenter.song.sample_rate) #pylint: disable=E1101
            self.audio_file = '{0}/{1}'.format(self.media_folder_name, file_name)
        else:
            raise ValueError('Create Audio File was called but there is no WF for segment {0}'.format(str(self)))

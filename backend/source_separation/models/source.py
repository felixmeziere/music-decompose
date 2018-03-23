"""
Defines the Source model.
"""
import uuid
from django.db import models
from django.contrib.postgres.fields import ArrayField
from audiofield.fields import AudioField
from music_decompose.services import rank_4_audacity, write_WF
class Source(models.Model):
    """
        Holds meta information and audio file on a Source
    """
    # DB fields
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    added_at = models.DateTimeField(auto_now_add=True)
    source_index = models.PositiveSmallIntegerField()
    source_separator = models.ForeignKey('source_separation.SourceSeparator', on_delete=models.CASCADE, related_name='sources')
    segment_group = ArrayField(models.IntegerField(null=True), null=True)
    audio_file = AudioField(blank=True, ext_whitelist=('.wav'), help_text=('Allowed type: .wav'))

    def __str__(self):
        return 'Source {0} of Song {1}'.format(self.source_index, str(self.source_separator.segmenter.song)) #pylint: disable=E1101

    class Meta:
        unique_together = ('source_index', 'source_separator',)

    def __init__(self, *args, source_WF=None, **kwargs):
        super(Source, self).__init__(*args, **kwargs)
        self.source_WF = source_WF


    @property
    def media_folder_name(self):
        """
        Folder where all this source's-related files will be
        Relative path from /medias
        """
        return '{0}/sources'.format(self.source_separator.media_folder_name) #pylint: disable=E1101

    @property
    def absolute_folder_name(self):
        """
        Folder where all this source's-related files will be
        Absolute path from root of project
        """
        return '{0}/sources'.format(self.source_separator.absolute_folder_name) #pylint: disable=E1101

    def write_audio_file(self):
        """
        Create or overwrite audio file and attach to instance
        """
        if self.source_WF is not None:
            file_name = '{0}.{1}'.format(rank_4_audacity(self.source_index), 'wav')
            write_WF(self.source_WF, '{0}/{1}'.format(self.absolute_folder_name, file_name), self.source_separator.segmenter.song.sample_rate) #pylint: disable=E1101
            self.audio_file = '{0}/{1}'.format(self.media_folder_name, file_name)
        else:
            raise ValueError('Create Audio File was called but there is no WF for source {0}'.format(str(self)))

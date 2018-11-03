"""
Abstract model to represent Output of Processor and store the corresponding audio
"""

from django.db import models
from audiofield.fields import AudioField
from music_decompose.services import rank_4_audacity, write_WF
from .container import Container


class Output(Container):    # pylint: disable=W0223
    """
    Output created by a Processor
    """

    class Meta:
        """
        Django Meta class
        """
        abstract = True
        unique_together = (
            'ind',
            'parent',
        )

    # Class attributes
    data_fields = ('WF', )

    # DB fields
    ind = models.PositiveIntegerField(verbose_name='Index')
    audio_file = AudioField(blank=True, ext_whitelist=('.wav'), help_text=('Allowed type: .wav'), max_length=500)

    def __init__(self, *args, **kwargs):
        super(Output, self).__init__(*args, **kwargs)
        if not set(('parent', 'ind')) <= set(self.unique_together):
            raise TypeError('unique_together should start with \'parent\' and \'ind\'.')

    def __str__(self):
        return '{0} {1} for Song: {2}'.format(self.__class__.__name__, self.ind, self.song)

    @property
    def media_folder_name(self):
        """
        Folder where all this Output's-related files will be
        Relative path from /media
        """
        return '{0}/{1}s'.format(self.parent.media_folder_name, self.__class__.__name__)

    def write_audio_file(self):
        """
        Create or overwrite audio file and attach to instance
        """
        if self.WF is not None:
            file_name = '{0}.{1}'.format(rank_4_audacity(self.ind), 'wav')
            write_WF(self.WF, '{0}/{1}'.format(self.absolute_folder_name, file_name), self.parent.song.sample_rate)    #pylint: disable=E1101
            self.audio_file = '{0}/{1}'.format(self.media_folder_name, file_name)
        else:
            raise ValueError('Write Audio File was called but there is no WF for segment {0}'.format(str(self)))

    @property
    def data_path(self):
        pass

    @property
    def path_in_hdf5(self):
        pass

"""
Defines the Song model.
"""
import re
import librosa as lr
from django.db import models
from audiofield.fields import AudioField
from music_decompose.models import Processor

def get_upload_path(instance, _):
    """
    Get file upload path that depends on song name
    """
    file_path = '{0}/original_{1}.wav'.format(instance.sanitized_name, instance.title)
    return file_path

class Song(Processor):
    """
    Holds meta information on a song and link to files.
    """
    # Class attributes
    data_fields = ('song_WF',)

    # DB fields
    title = models.CharField(max_length=200, unique=True)
    tempo = models.FloatField(null=True, blank=True)
    sample_rate = models.PositiveIntegerField(blank=True, default=44100)
    original_file = AudioField(upload_to=get_upload_path,
                               blank=True,
                               ext_whitelist=('.wav'),
                               help_text=('Allowed type: .wav'),
                               max_length=500)

    def __str__(self):
        return '{0}'.format(self.title)

    @property
    def sanitized_name(self):
        """
        Name suitable for file naming
        """
        return re.sub(r'[^a-zA-Z0-9]', '', self.title)

    @property
    def song(self):
        """
        To match _Container
        """
        return self

    def import_song_WF(self):
        """
        Import WF from wav file to self.song_WF
        """
        self.song_WF = lr.load(self.original_file.path, self.sample_rate)[0] #pylint: disable=W0201

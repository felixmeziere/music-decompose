"""
Defines the Song model.
"""
import uuid
import re
import librosa as lr
from django.db import models
from audiofield.fields import AudioField
from music_decompose.services import load_fields_from_hdf5, save_fields_to_hdf5
from music_decompose.constants import STATUS_CHOICES

def get_upload_path(instance, _):
    """
    Get file upload path that depends on song name
    """
    file_path = '{0}/original_{1}.wav'.format(instance.sanitized_name, instance.title)
    return file_path

class Song(models.Model):
    """
    Holds meta information on a song and link to files.
    """
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    added_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200, unique=True)
    tempo = models.FloatField(null=True, blank=True)
    sample_rate = models.PositiveIntegerField(blank=True, default=44100)
    original_file = AudioField(upload_to=get_upload_path,
                               blank=True,
                               ext_whitelist=('.wav'),
                               help_text=('Allowed type: .wav'))
    tempo_estimation_status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='not_started')
    data_path = models.CharField(max_length=500, null=True)

    def __str__(self):
        return '{0}'.format(self.title)

    def __init__(self, *args, song_WF=None, **kwargs):
        super(Song, self).__init__(*args, **kwargs)
        self._song_WF = song_WF
        if not self.data_path:
            self.data_path = 'music_decompose/media/{0}/song_{1}.hdf5'.format(self.sanitized_name, self.sanitized_name)

    @property
    def sanitized_name(self):
        """
        Name suitable for file naming
        """
        return re.sub(r'[^a-zA-Z0-9]', '', self.title)

    @property
    def song_WF(self):
        """
        The waveform of the song
        """
        if self._song_WF is None:
            load_fields_from_hdf5(self, ['song_WF'])
            if self._song_WF is None:
                self.import_song_WF()
        return self._song_WF

    def dump_data(self):
        """
        Dump instance data to disk
        """
        fields = (
            'song_WF',
        )
        save_fields_to_hdf5(self, fields)

    def import_song_WF(self):
        """
        Import WF from wav file to self.song_WF
        """
        self._song_WF = lr.load(self.original_file.path, self.sample_rate)[0]

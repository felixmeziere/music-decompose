"""
Defines the Song model.
"""
import re
import librosa as lr
from django.db import models
from audiofield.fields import AudioField
from music_decompose.models import Container
from song.tasks import run_full_flow_for_song

def get_upload_path(instance, _):
    """
    Get file upload path that depends on song name
    """
    file_path = '{0}/{1}.wav'.format(instance.sanitized_name, instance.title)
    return file_path

class Song(Container):
    """
    Holds meta information on a song and link to files.
    """
    # Class attributes
    data_fields = ('song_WF',)

    # DB fields
    title = models.CharField(max_length=200, unique=True)
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
    def data_path(self):
        """
        HDF5 file containing heavy data
        """
        return 'music_decompose/media/{0}/data.hdf5'.format(self.song.sanitized_name)

    @property
    def path_in_hdf5(self):
        """
        Path with data related to Song instance in the hdf5
        """
        return '/'

    @property
    def media_folder_name(self):
        """
        Folder where all this Processor's-related files will be
        Relative path from /media
        """
        return '{0}'.format(self.song.sanitized_name)

    def import_song_WF(self):
        """
        Import WF from wav file to self.song_WF
        """
        self.song_WF = lr.load(self.original_file.path, self.sample_rate)[0] #pylint: disable=W0201

    def run_full_flow(self, asynch=True):
        """
        Call run_full_flow_for_song on this song
        """
        if asynch:
            function = run_full_flow_for_song.delay
        else:
            function = run_full_flow_for_song
        function(self.uuid)

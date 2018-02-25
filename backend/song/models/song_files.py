"""
    Model to wrap all Audio Files for a song
"""
import uuid
from django.db import models
from audiofield.fields import AudioField
from .song import Song
from music_decompose.services import create_directory_if_needed

def get_upload_path(instance, _):
    directory = '{0}/original_song'.format(instance.song.sanitized_name)
    create_directory_if_needed(directory)
    return directory

class SongFiles(models.Model):
    """
        Handle Audio Files of a song.
    """
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    added_at = models.DateTimeField(auto_now_add=True)
    original_file = AudioField(upload_to=get_upload_path,
                               blank=True,
                               ext_whitelist=('.wav'),
                               help_text=('Allowed type: .wav'))
    song = models.OneToOneField(
        Song,
        on_delete=models.CASCADE,
        blank=True,
        related_name='files',
    )


    class Meta:
        """
            Django Meta Class.
        """
        verbose_name_plural = "Song Files"

    def __str__(self):
        return 'Audio files for {0}'.format(self.song)


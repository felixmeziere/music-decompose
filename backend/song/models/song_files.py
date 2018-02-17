"""
    Defines the song model.
"""
import uuid
from django.db import models
from audiofield.fields import AudioField
from django.conf import settings
from django.utils.html import format_html
from .song import Song

class SongFiles(models.Model):
    """
        Handle Audio Files of a song.
    """
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    added_at = models.DateTimeField(auto_now_add=True)
    original_file = AudioField(upload_to='original_songs/',
                        blank=True,
                        ext_whitelist=('.wav'),
                        help_text=('Allowed type: .wav'))
    song = models.OneToOneField(
        Song,
        on_delete=models.CASCADE,
        blank=True,
        related_name='files',
    )

    def audio_file_player(self):
        """
            Audio player tag for admin
        """
        if self.original_file:
            file_url = settings.MEDIA_URL + str(self.original_file)
            player_string = format_html('<audio src="%s" controls>Your browser does not support the audio element.</audio>' % (file_url))
            return player_string

    audio_file_player.allow_tags = True
    audio_file_player.short_description = ('Audio file player')


    class Meta:
        """
            Django Meta Class.
        """
        verbose_name_plural = "Song Files"

    def __str__(self):
        return 'Audio files for {0}'.format(self.song)

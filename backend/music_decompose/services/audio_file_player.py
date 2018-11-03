"""
   Audio File Player to be used in any admin
"""
from django.conf import settings
from django.utils.html import format_html


def audio_file_player(audio_file):    #pylint: disable=R0201
    """
        Audio player tag for admin
    """
    if audio_file:
        file_url = settings.MEDIA_URL + str(audio_file)
        player_string = format_html('<audio src="%s" controls>Your browser does\
                not support the audio element.</audio>' % (file_url))
        return player_string
    return None

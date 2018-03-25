"""
song django app config
"""
from django.apps import AppConfig

class SongConfig(AppConfig):
    """
    Django config class
    """
    name = 'song'
    verbose_name = 'Song'

    def ready(self):
        import song.signals #pylint: disable=W0612

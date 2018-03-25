"""
source_separation django app config
"""
from django.apps import AppConfig

class SourceSeparationConfig(AppConfig):
    """
    Django config class
    """
    name = 'source_separation'
    verbose_name = 'Source Separation'

    def ready(self):
        import source_separation.signals #pylint: disable=W0612

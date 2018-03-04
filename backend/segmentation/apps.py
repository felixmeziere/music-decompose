"""
segmentation django app config
"""
from django.apps import AppConfig

class SegmentationConfig(AppConfig):
    """
    Django config class
    """
    name = 'segmentation'
    verbose_name = 'Segmentation'

    def ready(self):
        import segmentation.signals #pylint: disable=W0612

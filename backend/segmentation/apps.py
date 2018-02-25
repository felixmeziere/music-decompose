from django.apps import AppConfig
from django.db.models.signals import pre_delete

class SegmentationConfig(AppConfig):
    name = 'segmentation'
    verbose_name = 'Segmentation'

    def ready(self):
        import segmentation.signals



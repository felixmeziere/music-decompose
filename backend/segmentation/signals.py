import os
import soundfile as sf
from django.dispatch import receiver
from django.db.models.signals import pre_delete, pre_save
from django.conf import settings
from segmentation.models import Segment


@receiver(pre_delete, sender=Segment)
def remove_audio_file_pre_delete(sender, instance, using, **kwargs):
    """
    Ensures the associated audio file is deleted
    when Segment instance is deleted
    """
    if instance.audio_file:
        if os.path.isfile(instance.audio_file.path):
            os.remove(instance.audio_file.path)

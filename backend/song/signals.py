"""
Django signals for app segmentation. Allow to run code automatically on a few django lifecycle events.
"""
import os
from django.dispatch import receiver
from django.db.models.signals import pre_delete
from song.models import Song


@receiver(pre_delete, sender=Song)
def remove_original_file_pre_delete(sender, instance, using, **kwargs): # pylint: disable=W0613
    """
    Ensures the associated original audio file is deleted
    when Song instance is deleted
    """
    if instance.original_file:
        if os.path.isfile(instance.original_file.path):
            os.remove(instance.original_file.path)

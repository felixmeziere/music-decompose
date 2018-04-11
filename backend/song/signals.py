"""
Django signals for app segmentation. Allow to run code automatically on a few django lifecycle events.
"""
import shutil
import os
from django.dispatch import receiver
from django.db.models.signals import pre_delete
from song.models import Song
from music_decompose.models import Output
from music_decompose.models import Container


@receiver(pre_delete, sender=Song)
def remove_original_file_pre_delete(sender, instance, using, **kwargs): # pylint: disable=W0613
    """
    Ensures the associated original audio file is deleted
    when Song instance is deleted
    """
    if instance.original_file:
        if os.path.isfile(instance.original_file.path):
            os.remove(instance.original_file.path)


def remove_audio_file_pre_delete(sender, instance, using, **kwargs): # pylint: disable=W0613
    """
    Ensures the associated audio file is deleted
    when Output instance is deleted
    """
    if instance.audio_file:
        dirname = os.path.dirname(instance.audio_file.path)
        if os.path.isdir(dirname):
            shutil.rmtree(dirname)

def remove_data_pre_delete(sender, instance, using, **kwargs): # pylint: disable=W0613
    """
    Ensures all the associated of a Container is deleted
    when instance is deleted
    """
    if os.path.isdir(instance.absolute_folder_name):
        shutil.rmtree(instance.absolute_folder_name)
    if os.path.isfile(instance.data_path):
        os.remove(instance.data_path)

for model in Output.__subclasses__():
    pre_delete.connect(remove_audio_file_pre_delete, sender=model)

for model in Container.__subclasses__():
    pre_delete.connect(remove_data_pre_delete, sender=model)

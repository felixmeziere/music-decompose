"""
Django signals for app segmentation. Allow to run code automatically on a few django lifecycle events.
"""
import shutil
import os
from django.dispatch import receiver
from django.db.models.signals import pre_delete
from song.models import Song
from music_decompose.models import Output, Container
from music_decompose.services import remove_ndarrays_in_hdf5, get_leaf_submodels


@receiver(pre_delete, sender=Song)
def remove_original_file_pre_delete(sender, instance, using, **kwargs): # pylint: disable=W0613
    """
    Ensures the associated original audio file is deleted
    when Song instance is deleted
    """
    if instance.original_file:
        if os.path.isfile(instance.original_file.path):
            os.remove(instance.original_file.path)


def remove_audio_file_pre_delete_output(sender, instance, using, **kwargs): # pylint: disable=W0613
    """
    Ensures the associated audio file is deleted
    when Output instance is deleted
    """
    if instance.audio_file:
        dirname = os.path.dirname(instance.audio_file.path)
        if os.path.isdir(dirname):
            shutil.rmtree(dirname)

def remove_data_pre_delete_container(sender, instance, using, **kwargs): # pylint: disable=W0613
    """
    Ensures all the associated data of a Container is deleted
    when instance is deleted
    """
    if os.path.isdir(instance.absolute_folder_name):
        shutil.rmtree(instance.absolute_folder_name)
    if instance.data_path is not None and os.path.isfile(instance.data_path):
        remove_ndarrays_in_hdf5(
            instance.data_path,
            [instance._get_dataset_path(field) for field in instance.data_fields],
        )

for model in get_leaf_submodels(Output):
    pre_delete.connect(remove_audio_file_pre_delete_output, sender=model)

for model in get_leaf_submodels(Container):
    pre_delete.connect(remove_data_pre_delete_container, sender=model)

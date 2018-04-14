"""
Abstract model to handle storage paths
"""
import uuid
from django.db import models
from music_decompose.services import save_ndarrays_to_hdf5

class Container(models.Model):
    """
    Holds data and where that data is stored
    """
    # Class Attributes
    data_fields = ()

    # Django DB fields
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    added_at = models.DateTimeField(auto_now_add=True)
    parent = None

    class Meta:
        """
        Django Meta class
        """
        abstract = True

    def __str__(self):
        raise NotImplementedError

    def __init__(self, *args, **kwargs):
        for data_field in self.data_fields:
            try:
                value = kwargs.pop(data_field)
            except KeyError:
                value = None
            setattr(self, data_field, value)
        if len(self._meta.unique_together) > 1:
            raise ValueError('Container is not designed to have more than one unique_together tuple. Change that.')
        super(Container, self).__init__(*args, **kwargs)

    @property
    def unique_together(self):
        """
        Shortcut to return unique together from Meta class
        """
        if self._meta.unique_together:
            return self._meta.unique_together[0]
        return ()

    @property
    def media_folder_name(self):
        """
        Folder where all this container's-related files will be.
        Relative path from /medias
        """
        raise NotImplementedError

    @property
    def absolute_folder_name(self):
        """
        Folder where all this Container's-related files will be
        Relative path from root of project
        """
        return 'music_decompose/media/{0}'.format(self.media_folder_name)

    @property
    def song(self):
        """
        Parent initial Song Container
        """
        if self.__class__.__name__ == 'Song':
            return self
        return self.parent.song

    @property
    def data_path(self):
        """
        HDF5 file containing data_fields info
        """
        raise NotImplementedError

    @property
    def path_in_hdf5(self):
        """
        Path with data related to Container instance in the hdf5
        """
        raise NotImplementedError

    def _get_dataset_path(self, field):
        """
        Path to give to dataset inside hdf5 file
        """
        return '{0}{1}||{2}'.format(self.path_in_hdf5, field, self.uuid)

    def dump_data(self):
        """
        Dump instance data to disk
        """
        attr_names = [field for field in self.unique_together if field != 'parent']
        save_ndarrays_to_hdf5(
            self.data_path,
            [getattr(self, data_field) for data_field in self.data_fields],
            [self._get_dataset_path(field) for field in self.data_fields],
            attr_names,
            [getattr(self, attr_name) for attr_name in attr_names],
        )

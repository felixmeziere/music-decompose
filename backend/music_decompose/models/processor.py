"""
Abstract model to perform signal processing and store the Output
"""

from django.db import models
from music_decompose.constants import STATUS_CHOICES
from music_decompose.services import save_fields_to_hdf5
from ._container import Container

class Processor(Container): # pylint: disable=W0223
    """
    Container that processes an input and creates Outputs.
    """

    class Meta:
        """
        Django Meta class
        """
        abstract = True

    # Class attributes
    parameters = ()

    # DB fields
    processing_status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='not_started')

    def __init__(self, *args, **kwargs):
        super(Processor, self).__init__(*args, **kwargs)
        field_names = [field.name for field in self._meta.fields]
        for parameter in self.parameters:
            if not parameter in field_names:
                raise TypeError('All parameters of a Processor should be implemented as DB fields.')
        minimum_unique_together = self.parameters if (not hasattr(self, 'parent') or self.parent is None) else ('parent', ) + self.parameters
        if not set(minimum_unique_together) <= set(self.unique_together):
            raise TypeError('unique_together should start with \'parent\' and the parameters of the Processor.')

    def __str__(self):
        pretty_params = ''
        for param in self.unique_together: # pylint: disable=E1133
            if param != 'parent':
                pretty_params += ' - {0}: {1}'.format(param, getattr(self, param))
        return '{0} for Song: {1}{2}'.format(self.__class__.__name__, self.song, pretty_params)

    @property
    def step_name_for_paths(self):
        """
        SP step usable in paths.
        """
        return self.__class__.__name__

    @property
    def data_path(self):
        """
        HDF5 file containing heavy data
        """
        return 'music_decompose/media/{0}/{1}/{2}/{3}.hdf5'.format(
            self.song.sanitized_name,
            self._meta.app_label,
            self.step_name_for_paths,
            self.song.sanitized_name + '-' + self.step_name_for_paths
        )

    @property
    def param_string(self):
        """
        Name containing parameters suitable for paths
        """
        param_string = ''
        if self.parent is not None:
            param_string += '{0}{1}'.format(
                self.parent.param_string + '||' if self.parent is not None else '',
                self.step_name_for_paths,
            )
        for param in self.unique_together: # pylint: disable=E1133
            if param != 'parent':
                param_string += '|{0}-{1}'.format(param, getattr(self, param))

        return param_string

    @property
    def media_folder_name(self):
        """
        Folder where all this Processor's-related files will be
        Relative path from /media
        """
        return '{0}/{1}/{2}/{3}'.format(self.song.sanitized_name, self._meta.app_label, self.step_name_for_paths, self.param_string)

    @property
    def absolute_folder_name(self):
        """
        Folder where all this Processor's-related files will be
        Relative path from root of project
        """
        return 'music_decompose/media/{0}'.format(self.media_folder_name)

    def dump_data(self):
        """
        Dump instance data to disk
        """
        save_fields_to_hdf5(self, self.data_fields)

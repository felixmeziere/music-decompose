"""
Abstract model to perform signal processing and store the Output
"""

from django.db import models
from music_decompose.constants import STATUS_CHOICES
from music_decompose.tasks import process_and_save
from .container import Container

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
        return self.song.data_path

    @property
    def path_in_hdf5(self):
        return '/{0}/{1}/'.format(
            self._meta.app_label,
            self.step_name_for_paths,
        )

    @property
    def media_folder_name(self):
        """
        Folder where all this Processor's-related files will be
        Relative path from /media
        """
        return '{0}/{1}/{2}/{3}'.format(self.song.sanitized_name, self._meta.app_label, self.step_name_for_paths, self.uuid)

    def _process_and_save(self):
        """
        Execute the purpose of the processor and save the results
        """
        raise NotImplementedError

    def process_and_save(self, asynch=True):
        """
        Execute _process_and_save in the background
        """
        if asynch:
            function = process_and_save.delay
        else:
            function = process_and_save
        function(self.uuid, self.__class__.__name__)

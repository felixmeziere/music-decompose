"""
Add fields and properties dynamically to abstract classes defined in this folder.
"""
import numpy as np
from music_decompose.services import load_ndarrays_from_hdf5

def get_data_field_getter(data_field):
    """
    Return the property getter customised with data_field.
    """
    def data_field_getter(self):
        """
        Return value of data_field. If value still not loaded in instance, load
        it from the hdf5 file.
        """
        value = getattr(self, '_' + data_field)
        if value is None:
            [value] = load_ndarrays_from_hdf5(
                self.data_path,
                [self._get_dataset_path(data_field)],
            )
        return value
    return data_field_getter

def get_data_field_setter(data_field):
    """
    Return the property setter customised with data_field.
    """
    def data_field_setter(self, value):
        """
        Set value of data_field in the instance.
        """
        if value is not None and not isinstance(value, np.ndarray):
            raise TypeError('Only numpy arrays should be given to a Container as data_field')
        setattr(self, '_' + data_field, value)
    return data_field_setter


def make_container(ContainerSubClass):
    """
    Add custom properties to Container.
    - a getter and setter for each data_field
    """
    for data_field in ContainerSubClass.data_fields:
        setattr(ContainerSubClass, data_field, property(get_data_field_getter(data_field), get_data_field_setter(data_field)))

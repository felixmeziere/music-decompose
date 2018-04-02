"""
Add fields and properties dynamically to abstract classes defined in this folder.
"""
import numpy as np
from music_decompose.services import load_fields_from_hdf5

def get_data_field_getter(data_field):
    """
    Return the property getter customised with data_field.
    """
    def data_field_getter(self):
        """
        Return value of data_field. If value still not loaded in instance, load
        it from the hdf5 file.
        """
        if getattr(self, '_' + data_field) is None:
            load_fields_from_hdf5(self, [data_field])
        return getattr(self, '_' + data_field)
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
            raise TypeError('Only numpy arrays should be given as data_field to a Container')
        setattr(self, '_' + data_field, value)
    return data_field_setter


def make_processor(ProcessorSubClass):
    """
    Add custom properties to Processor.
    - a getter and setter for each data_field
    """
    for data_field in ProcessorSubClass.data_fields:
        setattr(ProcessorSubClass, data_field, property(get_data_field_getter(data_field), get_data_field_setter(data_field)))

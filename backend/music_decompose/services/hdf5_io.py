"""
Common I/O functions to handle hdf5 files
"""
import h5py
import numpy as np
from .audio_io import create_directory_for_file_if_needed
def get_hidden_field_name(field):
    """
    From field name, get corresponding instance attribute name
    that contains the data.
    """
    return '_{}'.format(field)

def load_fields_from_hdf5(instance, fields):
    """
    Load fields from hdf5 file to corresponding attributes in instance
    """
    with h5py.File(instance.data_path, 'r') as data_file:
        for field in fields:
            setattr(instance, get_hidden_field_name(field), data_file[field][()])

def save_fields_to_hdf5(instance, fields):
    """
    Save fields to hdf5 file from corresponding attributes in instance
    """
    create_directory_for_file_if_needed(instance.data_path)
    with h5py.File(instance.data_path, 'w') as data_file:
        for field in fields:
            value = getattr(instance, get_hidden_field_name(field))
            if isinstance(value, list):
                dtype = np.array(value).dtype
                shape = (len(value),)
            else:
                dtype = value.dtype
                shape = value.shape
            if value is not None:
                data_file.create_dataset(field, shape, dtype=dtype, data=value)

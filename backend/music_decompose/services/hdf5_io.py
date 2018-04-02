"""
Common I/O functions to handle hdf5 files
"""
import h5py
import numpy as np
from music_decompose.services.audio_io import create_directory_for_file_if_needed

def get_dataset_name(field, instance):
    return '{0}||{1}'.format(field, instance.param_string)


def load_fields_from_hdf5(instance, fields):
    """
    Load fields from hdf5 file to corresponding data_fields attributes in instance
    """
    try:
        with h5py.File(instance.data_path, 'r') as data_file:
            for field in fields:
                setattr(instance, field, data_file[get_dataset_name(field, instance)][()])
    except (FileNotFoundError, OSError):
        pass

def save_fields_to_hdf5(instance, fields):
    """
    Save fields to hdf5 file from corresponding data_fields attributes in instance
    """
    create_directory_for_file_if_needed(instance.data_path)
    with h5py.File(instance.data_path, 'w') as data_file:
        for field in fields:
            value = getattr(instance, field)
            if not isinstance(value, np.ndarray):
                raise TypeError('Only ndarrays should be saved to hdf5')
            dtype = value.dtype
            shape = value.shape
            if value is not None:
                dataset = data_file.create_dataset(get_dataset_name(field, instance), shape, dtype=dtype, data=value)
            for attr in instance.unique_together:
                if attr != 'parent':
                    value = getattr(instance, attr)
                    if isinstance(value, str):
                        value = np.string_(value) # pylint: disable=E1101
                    dataset.attrs.create(attr, value)

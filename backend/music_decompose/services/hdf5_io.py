"""
Common I/O functions to handle hdf5 files
"""
import h5py
import numpy as np
from music_decompose.services.audio_io import create_directory_for_file_if_needed


def load_ndarrays_from_hdf5(file_path, paths_in_hdf5):
    """
    Load paths_in_hdf5 from file_path hdf5 file.
    Return list with the corresponding ndarrays.
    """
    values = [None for path_in_hdf5 in paths_in_hdf5]
    with h5py.File(file_path, 'r') as data_file:
        for i, path_in_hdf5 in enumerate(paths_in_hdf5):
            try:
                values[i] = data_file[path_in_hdf5][()]
            except KeyError:
                pass
    return values


def remove_ndarrays_in_hdf5(file_path, paths_in_hdf5):
    """
    Within file_path hdf5 file, delete arrays at paths_in_hdf5
    """
    with h5py.File(file_path, 'a') as data_file:
        for path_in_hdf5 in paths_in_hdf5:
            try:
                if data_file.__contains__(path_in_hdf5):
                    del data_file[path_in_hdf5]
            except KeyError:
                pass


def save_ndarrays_to_hdf5(file_path, arrays, paths_in_hdf5, attr_names=(), attr_values=()):
    """
    Within file_path hdf5 file, save arrays at paths_in_hdf5 with attr_names and attr_values.
    """
    create_directory_for_file_if_needed(file_path)
    remove_ndarrays_in_hdf5(file_path, paths_in_hdf5)
    with h5py.File(file_path, 'a') as data_file:
        for i, array in enumerate(arrays):
            path_in_hdf5 = paths_in_hdf5[i]
            if array is not None:
                if not isinstance(array, np.ndarray):
                    raise TypeError('Only ndarrays should be saved to hdf5')
                dtype = array.dtype
                shape = array.shape
                dataset = data_file.create_dataset(path_in_hdf5, shape, dtype=dtype, data=array)
                for j, attr_name in enumerate(attr_names):
                    attr_value = attr_values[j]
                    if isinstance(attr_value, str):
                        attr_value = np.string_(attr_value)    # pylint: disable=E1101
                    dataset.attrs.create(attr_name, attr_value)

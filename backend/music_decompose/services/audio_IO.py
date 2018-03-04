"""
Reusable functions relative to Audio I/O.
"""
import os
import soundfile as sf
import numpy as np
from django.conf import settings

def rank_4_audacity(i):
    """
    Used to format the indexes with preceding zeros so that
    Audacity orders them correctly.
    """
    n_zeros = 4 - len(str(i))
    return '{0}{1}'.format('0' * n_zeros, str(i))


def create_directory_if_needed(directory_name):
    """
    Check if directory exists. If not, creates it.
    """
    if not os.path.isdir(directory_name):
        os.makedirs(directory_name)


def create_directory_for_file_if_needed(file_name):
    """
    From a file name, create directory supposed to contain it.
    """
    directory_name = os.path.dirname(file_name)
    create_directory_if_needed(directory_name)
    return directory_name


def write_WF(WF, file_name, sample_rate):
    """
    Write one waveform to one file, creating directory if needed first
    """
    create_directory_for_file_if_needed(file_name)
    sf.write(file_name, WF, sample_rate)


def write_WFs(folder, filename_prefix='', indices=None, WFs=None, extension=settings.HEAVY_AUDIO_WRITE_EXTENSION, sample_rate=settings.DEFAULT_SAMPLE_RATE):
    """
    Save a list of WFs or np Array of WFs to a folder, with the specified indices and
    filename prefix. Use specified format.
    """
    if WFs is None:
        raise ValueError('save_WFs expects either a WF list or 2-D np array')

    is_array = isinstance(WFs, np.ndarray)
    if is_array:
        n_WFs = WFs.shape[0]
    else:
        n_WFs = len(WFs)

    if indices is None:
        indices = range(n_WFs)
    if len(indices) != n_WFs:
        raise ValueError('save_WFs expects as many indices as there are WFs')

    file_names = []
    file_paths = []
    for i in indices:
        file_name = '{0}_{1}.{2}'.format(filename_prefix, rank_4_audacity(i), extension)
        file_path = '{0}/{1}'.format(folder, file_name)
        if is_array:
            sf.write(file_path, WFs[i, :], sample_rate)
        else:
            sf.write(file_path, WFs[i], sample_rate)
        file_names.append(file_name)
        file_paths.append(file_path)

    return file_paths, file_names

from song.models import Song
from segmentation.models import Segmenter
import numpy as np
import h5py
import numpy as np
from music_decompose.services.audio_io import create_directory_for_file_if_needed
seg = Segmenter.objects.first()
song = Song.objects.first()
# song.import_song_WF()
# song.dump_data()
# song.song_WF = np.array([2,2,2,3,4,5,5,])
# song.dump_data()
# seg.segment_WFs = np.array([1,2,4])
# seg.segment_WFs = np.array([1,2,4])
# seg.dump_data()
# def get_dataset_path(field, instance):
#     """
#     Path to give to dataset inside hdf5 file
#     """
#     return '{0}/{1}||{2}'.format(instance.path_in_hdf5, field, instance.uuid)
# instance = seg
# field = 'segment_WFs'
# value = getattr(instance, field)
# data_file = h5py.File(instance.data_path, 'a')
# if not isinstance(value, np.ndarray):
#     raise TypeError('Only ndarrays should be saved to hdf5')
# dtype = value.dtype
# shape = value.shape
# if value is not None:
#     if not data_file.__contains__(instance.path_in_hdf5):
#         data_file.create_group(instance.path_in_hdf5)
#     del data_file[get_dataset_path(field, instance)]
#     dataset = data_file.create_dataset(get_dataset_path(field, instance), shape, dtype=dtype, data=value)
# for attr in instance.unique_together:
#     if attr != 'parent':
#         value = getattr(instance, attr)
#         if isinstance(value, str):
#             value = np.string_(value) # pylint: disable=E1101
#         dataset.attrs.create(attr, value)
# data_file.close()

from celery import shared_task
from segmentation.models import Segmenter
from source_separation.models import SegmentGrouper, SourceExtractor
from song.models import Song, TempoEstimator


song.tempo_estimators.all().delete()
tempo_estimator = TempoEstimator.objects.create(
    parent=song,
    method='classic',
)
tempo_estimator.process_and_save(asynch=False)
segmenter = Segmenter.objects.create(
    parent=tempo_estimator,
    method='blind',
    n_tempo_lags_per_segment=4,
)
segmenter.process_and_save(asynch=False)
segment_grouper = SegmentGrouper.objects.create(
    parent=segmenter,
    method='classic',
)
segment_grouper.process_and_save(asynch=False)
source_extractor = SourceExtractor.objects.create(
    parent=segment_grouper,
    method='classic',
)
source_extractor.process_and_save(asynch=False)

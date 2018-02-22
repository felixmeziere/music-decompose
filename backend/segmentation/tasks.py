from __future__ import absolute_import, unicode_literals
import time
from celery import shared_task
from segmentation.models import SegmentList, Segment
import h5py
import os
import librosa as lr
import soundfile as sf
import numpy as np

@shared_task
def compute_segmentation(segment_list_uuid):
    segment_list = SegmentList.objects.get(pk=segment_list_uuid)
    segment_list.segmentation_status = 'pending'
    segment_list.save()
    segment_limits_IS = [i * 60000 for i in range(200)]
    song_WF, _ = lr.load(segment_list.song.files.original_file.path, 44100)
    segment_indices = range(len(segment_limits_IS)-1)
    def rank_4_audacity(i):
        n_zeros = 4 - len(str(i))
        return '{0}{1}'.format('0' * n_zeros, str(i))

    folder = 'music_decompose/media/{0}'.format(segment_list.folder_name)

    Segment.objects.filter(segment_list__method=segment_list.method, segment_list=segment_list).delete()
    segment_WFs = []
    segments = []
    for i in segment_indices:
        start = segment_limits_IS[i]
        end = segment_limits_IS[i+1]
        segment_WF = song_WF[start:end]
        segment_WFs.append(segment_WF)
        filename = '{0}.flac'.format(rank_4_audacity(i))
        filepath = '{0}/segments/{1}'.format(folder, filename)
        sf.write(filepath, segment_WF, 44100)
        segments.append(Segment(
            index=i,
            segment_list=segment_list,
            length_in_samples=end - start,
            start_position_in_samples=start,
            end_position_in_samples=end,
            audio_file='{0}/segments/{1}'.format(segment_list.folder_name, filename),
        ))

    with h5py.File('{0}/segmentation_{1}.hdf5'.format(folder, segment_list.song.sanitized_name), 'w') as f:
        f.create_dataset('segment_limits_IS', (len(segment_limits_IS),), dtype='i', data=segment_limits_IS)
        f.create_dataset('segment_WFs', (len(segment_WFs), len(segment_WFs[0])), dtype='f', data=np.array(segment_WFs))
        segment_list.data_path = f.filename
        segment_list.save()

    Segment.objects.bulk_create(segments)
    segment_list.segmentation_status = 'done'
    segment_list.save()



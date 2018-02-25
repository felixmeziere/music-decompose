from segmentation.models import SegmentList, Segment
import h5py
import librosa as lr
import soundfile as sf
import numpy as np
import os

def compute_segmentation(segment_list_uuid):
    segment_list = SegmentList.objects.get(pk=segment_list_uuid)
    segment_list.segmentation_status = 'pending'
    segment_list.save()
    try:
        ### Load data
        song_WF, _ = lr.load(segment_list.song.files.original_file.path, 44100)


        ### Detect segment limits
        segment_limits_IS = [i * 60000 for i in range(200)]


        ### Save data
        segment_WFs = []
        for i in range(len(segment_limits_IS)-1):
            segment_WF = song_WF[segment_limits_IS[i]:segment_limits_IS[i+1]]
            segment_WFs.append(segment_WF)

        segment_list.segments.all().delete()
        segments = []
        for i, segment_WF in enumerate(segment_WFs):
            segment = Segment(
                segment_index=i,
                segment_list=segment_list,
                length_in_samples=len(segment_WF),
                start_position_in_samples=segment_limits_IS[i],
                end_position_in_samples=segment_limits_IS[i+1],
                WF=segment_WF,
            )
            segment.write_audio_file()
            segments.append(segment)
        Segment.objects.bulk_create(segments)

        with h5py.File('{0}/segmentation_{1}.hdf5'.format(segment_list.absolute_folder_name, segment_list.song.sanitized_name), 'w') as f:
            f.create_dataset('segment_limits_IS', (len(segment_limits_IS),), dtype='i', data=segment_limits_IS)
            f.create_dataset('segment_WFs', (len(segment_WFs), len(segment_WFs[0])), dtype='f', data=np.array(segment_WFs))
            segment_list.data_path = f.filename

        segment_list.segmentation_status = 'done'
        segment_list.save()
    except Exception as e:
        segment_list.segmentation_status = 'failed'
        segment_list.save()
        raise e

from segmentation.models import SegmentList, Segment
import h5py
import librosa as lr
import soundfile as sf
import numpy as np
import os

def compute_segmentation(segment_list_uuid):
    ### Initialise
    segment_list = SegmentList.objects.get(pk=segment_list_uuid)
    segment_list.segmentation_status = 'pending'
    segment_list.save()
    try:
        ### Load data
        song_WF, _ = lr.load(segment_list.song.files.original_file.path, 44100)


        ### Detect segment limits
        if segment_list.method == 'blind':
            n_samples_per_tempo_lag = int((segment_list.song.sample_rate * 60) / segment_list.song.tempo)
            n_samples_per_segment = n_samples_per_tempo_lag * segment_list.n_tempo_lags_per_segment
            n_segments = int(len(song_WF) / n_samples_per_segment) + 1
            segment_starts_IS = np.zeros(n_segments)
            segment_starts_IS = [i * n_samples_per_tempo_lag * 8 for i in range(n_segments)]


        ### Save data
        segment_list.segment_starts_IS = segment_starts_IS
        segment_list.create_segment_WFs(song_WF)
        segment_list.dump_data()
        segment_list.create_segments()
        segment_list.save()

        ### End
        segment_list.segmentation_status = 'done'
        segment_list.save()
    except Exception as e:
        segment_list.segmentation_status = 'failed'
        segment_list.save()
        raise e

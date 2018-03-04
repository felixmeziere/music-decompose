
"""
Segment the segmenter.song.song_WF and then save all the related data
"""
import numpy as np

def compute_segmentation(method, song_WF, sample_rate, tempo, n_tempo_lags_per_segment):
    """
    Given segmenter object, do the segmentation and return the segment limits
    """
    ### Detect segment limits
    if method == 'blind':
        n_samples_per_tempo_lag = int((sample_rate * 60) / tempo)
        n_samples_per_segment = n_samples_per_tempo_lag * n_tempo_lags_per_segment
        n_segments = int(len(song_WF) / n_samples_per_segment) + 1
        segment_starts_IS = np.array([i * n_samples_per_segment for i in range(n_segments)])
    return segment_starts_IS

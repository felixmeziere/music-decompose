"""
Segment the song and return the semgent start samples
"""
import numpy as np


def compute_segmentation(method, song_WF, sample_rate, tempo, n_tempo_lags_per_segment):
    """
    Do the segmentation and return the segment starts
    """
    ### Detect segment limits
    if method == 'blind':
        n_samples_per_tempo_lag = int((sample_rate * 60) / tempo)
        n_samples_per_segment = n_samples_per_tempo_lag * n_tempo_lags_per_segment
        n_segments = int(len(song_WF) / n_samples_per_segment) + 1
        segment_starts_IS = np.array([i * n_samples_per_segment for i in range(n_segments)])
    return segment_starts_IS

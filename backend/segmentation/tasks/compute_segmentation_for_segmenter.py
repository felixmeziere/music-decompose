"""
compute_segmentation from segmenter data and store results in segmenter.
"""
from segmentation.sp_functions import compute_segmentation


def compute_segmentation_for_segmenter(segmenter):
    """
    Manipulations to do on Segmenter instance to store results of segmentation
    """
    ### Detect segment limits
    segment_starts_IS = compute_segmentation(
        segmenter.method,
        segmenter.song.song_WF,
        segmenter.song.sample_rate,
        segmenter.tempo,
        segmenter.n_tempo_lags_per_segment,
    )

    ### Save data
    segmenter.segment_starts_IS = segment_starts_IS
    segmenter.create_segment_WFs()
    segmenter.create_segments()
    segmenter.dump_data()
    segmenter.save()

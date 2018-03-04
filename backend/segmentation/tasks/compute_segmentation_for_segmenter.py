"""
compute_segmentation from segmenter data and store results in segmenter.
"""

from segmentation.sp_functions import compute_segmentation
from segmentation.models import Segmenter

def compute_segmentation_for_segmenter(segmenter_uuid):
    """
    The function
    """
    ### Initialise
    segmenter = Segmenter.objects.get(pk=segmenter_uuid)
    segmenter.segmentation_status = 'pending'
    segmenter.save()

    try:
        ### Detect segment limits
        segment_starts_IS = compute_segmentation(
            segmenter.method,
            segmenter.song.song_WF,
            segmenter.song.sample_rate,
            segmenter.tempo,
            segmenter.n_tempo_lags_per_segment,
        )

        ### Save data
        segmenter._segment_starts_IS = segment_starts_IS
        segmenter.create_segment_WFs()
        segmenter.create_segments()
        segmenter.dump_data()
        segmenter.save()

        ### End
        segmenter.segmentation_status = 'done'
        segmenter.save()
    except Exception as error:
        segmenter.segmentation_status = 'failed'
        segmenter.save()
        raise error

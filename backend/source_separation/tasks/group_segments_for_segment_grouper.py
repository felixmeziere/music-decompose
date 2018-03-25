"""
compute_source_separation from SourceExtractor data and store results in SourceExtractor.
"""

from source_separation.sp_functions import group_segments


def group_segments_for_segment_grouper(segment_grouper):
    """
    The function
    """

    ### Detect segment limits
    segment_groups = group_segments(
        segment_grouper.method,
        segment_grouper.segmenter.segment_WFs,
    )

    ### Save data
    segment_grouper._segment_groups = segment_groups
    segment_grouper.dump_data()
    segment_grouper.save()

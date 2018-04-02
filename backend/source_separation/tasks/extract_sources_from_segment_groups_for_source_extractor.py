"""
Get the source WFs from the segment groups
"""

from source_separation.sp_functions import extract_sources_from_segment_groups

def extract_sources_from_segment_groups_for_source_extractor(source_extractor):
    """
    Manipulations to do on the source_extractor to get and save the segment groups
    """

    ### Detect segment limits
    _, source_WFs = extract_sources_from_segment_groups(
        source_extractor.method,
        source_extractor.segment_grouper.segment_groups,
        source_extractor.segment_grouper.segmenter.segment_WFs,
    )

    ### Save data
    source_extractor.source_WFs = source_WFs
    source_extractor.create_sources()
    source_extractor.dump_data()
    source_extractor.save()

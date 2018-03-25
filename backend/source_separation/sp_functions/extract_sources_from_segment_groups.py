"""
From the segment groups, extract the source WFs
"""
import numpy as np

def extract_sources_from_segment_groups(method, segment_groups, segment_WFs):
    """
    Do the source separation from the segment groups
    """
    ### Extract sources
    if method == 'classic':
        source_WF = np.concatenate(segment_WFs)
        source_WFs = np.array([source_WF, source_WF])
        source_segment_WFs = np.array([segment_WFs, segment_WFs])
    return source_segment_WFs, source_WFs

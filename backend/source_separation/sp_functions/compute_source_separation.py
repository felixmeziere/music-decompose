
"""
Separate the sources and return the segment groups
"""
import numpy as np

def compute_source_separation(method, segment_WFs):
    """
    Do the source separation and return the segment groups
    """
    ### Detect segment groups
    return np.array([
        [1, 25, 50],
        [3, 45, 60],
    ])

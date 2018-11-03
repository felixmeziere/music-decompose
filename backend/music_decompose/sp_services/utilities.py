"""
Convenience functions for signal processing operations
"""

import numpy as np


def get_complementary(sub_array, size_of_original_array):
    """
    From range of integers extract integers not in sub_array and smaller than size_of_original_array
    """
    return np.setdiff1d(np.arange(size_of_original_array), sub_array)

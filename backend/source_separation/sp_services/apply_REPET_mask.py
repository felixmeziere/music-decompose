"""
Apply mask to segment STFTs, separating the sources.
Return rest and source segment STFTs.
"""
import numpy as np

def apply_REPET_mask(
        segment_STFTs,
        mask,
        upper_magnet_threshold,
        lower_magnet_threshold,
        hard_threshold,
    ):
    """
    Apply mask to segment STFTs, separating the sources.
    Return rest and source segment STFTs.
    """
    mask[mask > upper_magnet_threshold] = 1
    mask[mask <= lower_magnet_threshold] = 0
    source_segment_STFTs = np.multiply(segment_STFTs, mask)
    rest_segment_STFTs = segment_STFTs - source_segment_STFTs
    rest_spectros = np.abs(rest_segment_STFTs)
    if len(rest_spectros.shape) > 2:
        for i in np.arange(rest_spectros.shape[0]):
            max_rest_spectros = np.max(rest_spectros[i, :, :])
            rest_segment_STFTs[i, :, :][rest_spectros[i, :, :] < max_rest_spectros * hard_threshold] = 0
    else:
        max_rest_spectros = np.max(rest_spectros)
        rest_segment_STFTs[rest_spectros < max_rest_spectros * hard_threshold] = 0

    return rest_segment_STFTs, source_segment_STFTs

"""
From the segment groups, extract the source WFs
"""
import copy
import numpy as np
from music_decompose.sp_services import get_complementary, STFTs_to_WFs
from source_separation.sp_services import apply_REPET_mask


def extract_sources_from_segment_groups(method, segment_groups, segment_STFTs, hop_length, win_length):
    """
    Do the source separation from the segment groups
    """
    segment_STFTs = copy.copy(segment_STFTs)
    n_segments = segment_STFTs.shape[0]
    sources_segment_STFTs = []
    sources_segment_WFs = []
    # Extract sources
    if method == 'classic':
        for segment_group in segment_groups:
            extracted_indices = get_complementary(segment_group, n_segments)
            rest_segment_STFTs, source_segment_STFTs = _extract_group_source(segment_STFTs, extracted_indices, segment_group)
            segment_STFTs[extracted_indices, :, :] = rest_segment_STFTs
            del rest_segment_STFTs
            sources_segment_STFTs.append(source_segment_STFTs)
            sources_segment_WFs.append(STFTs_to_WFs(source_segment_STFTs, hop_length, win_length))
        sources_segment_STFTs.append(segment_STFTs)
        sources_segment_WFs.append(STFTs_to_WFs(segment_STFTs, hop_length, win_length))
        source_WFs = [np.concatenate(source_segment_WFs) for source_segment_WFs in sources_segment_WFs]
        min_length = min([len(source_WF) for source_WF in source_WFs])
        for i, source_WF in enumerate(source_WFs):
            source_WFs[i] = source_WF[:min_length]
        source_WFs = np.stack(source_WFs)
    return sources_segment_WFs, source_WFs


def _extract_group_source(
        segment_STFTs,
        group_to_be_modified,
        group_extracting,
        mask_upper_magnet_threshold=0.9,
        mask_lower_magnet_threshold=0.1,
        mask_hard_threshold=0,
        median_decision_threshold=0,
):
    """
    Apply REPET mask to segments in group_to_be_modified to subtract sound of
    segments in group_extracting from them.
    Source will be sound remaining in group_to_be_modified after subtraction i.e.
    not contained in segments of group_extracting.
    """
    if isinstance(group_extracting, int) or len(group_extracting) == 1:
        group_extracting_max_spectro = np.abs(segment_STFTs[group_extracting, :, :])
    else:
        group_extracting_max_spectro = np.max(np.abs(segment_STFTs[group_extracting, :, :]), axis=0)
    segment_STFTs_to_be_modified = segment_STFTs[group_to_be_modified, :, :]
    segment_spectros_to_be_modified = np.abs(segment_STFTs_to_be_modified)
    subtracted_spectros = segment_spectros_to_be_modified - group_extracting_max_spectro
    subtracted_spectros[subtracted_spectros < 0] = 0
    mask = np.divide(subtracted_spectros, segment_spectros_to_be_modified)
    mask[np.isnan(mask)] = 0
    rest_segment_STFTs, source_segment_STFTs = apply_REPET_mask(
        segment_STFTs_to_be_modified,
        mask,
        mask_upper_magnet_threshold,
        mask_lower_magnet_threshold,
        mask_hard_threshold,
    )

    # Return to the "rest" the sound that is too different from median of the segments of the group
    source_spectros = np.abs(source_segment_STFTs)
    source_median_spectro = np.median(source_spectros, axis=0)
    min_matrix = np.array([np.minimum(source_median_spectro, source_spectros[i, :, :]) for i in np.arange(source_spectros.shape[0])])
    mask = np.divide(min_matrix, source_spectros)
    mask[np.isnan(mask)] = 0
    additional_rest_segment_STFTs, source_segment_STFTs = apply_REPET_mask(
        segment_STFTs_to_be_modified,
        mask,
        median_decision_threshold,
        median_decision_threshold,
        0,
    )
    rest_segment_STFTs = np.add(rest_segment_STFTs, additional_rest_segment_STFTs)

    return rest_segment_STFTs, source_segment_STFTs

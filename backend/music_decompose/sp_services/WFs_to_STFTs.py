"""
Transform 2-dim array of WFs to 3-dim array of STFTs
"""

import numpy as np
import librosa as lr


def WFs_to_STFTs(WFs, n_fft, hop_length, win_length):    #pylint: disable=C0103
    """
    Transform 2-dim array of WFs to 3-dim array of STFTs
    """
    return np.array([lr.core.stft(
        WF,
        n_fft=n_fft,
        hop_length=hop_length,
        win_length=win_length,
    ) for WF in WFs])


def STFTs_to_WFs(STFTs, hop_length, win_length):    #pylint: disable=C0103
    """
    Transform 3-dim array of STFTs to 2-dim array of WFs
    """
    return np.array([lr.core.istft(
        STFTs[i, :, :],
        hop_length=hop_length,
        win_length=win_length,
    ) for i in range(len(STFTs))])

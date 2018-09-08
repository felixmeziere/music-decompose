# """
# Concatenate WFs into one WF
# """
# import numpy as np

# def WFs_to_WF(WFs):
#     """
#     Concatenate WFs into one WF
#     """
#     if not WFs:
#         return np.array([])
#     segLenIS = WFs.shape[1]
#     if totalNSegments == None:
#         WF = np.concatenate(WFs)
#     else:
#         WF = np.concatenate([np.zeros(segLenIS) for i in np.arange(totalNSegments)])
#         for i in np.arange(len(segmentIndices)):
#             WF[segmentIndices[i]*segLenIS:(segmentIndices[i]+1)*segLenIS] = segmentWF[i,:]
#     return WF

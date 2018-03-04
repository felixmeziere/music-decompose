# pylint: skip-file
from segmentation.models import Segmenter, Segment
import librosa as lr


segmenter = Segmenter.objects.first()
song_WF, _ = lr.load(segmenter.song.original_file.path, 44100)
segment_starts = [i * 100000 for i in range(50)]
segment_WFs = []
for i in range(len(segment_starts)-1):
    segment_WF = song_WF[segment_starts[i]:segment_starts[i+1]]
    segment_WFs.append(segment_WF)

Segment.objects.create(
    segment_index=1,
    segmenter=segmenter,
    length_in_samples=3,
    start_position_in_samples=3,
    end_position_in_samples=6,
    WF=segment_WFs[0],
)

from segmentation.models import SegmentList, Segment
import librosa as lr


segment_list = SegmentList.objects.first()
song_WF, _ = lr.load(segment_list.song.files.original_file.path, 44100)
segment_starts = [i * 100000 for i in range(50)]
segment_WFs = []
for i in range(len(segment_starts)-1):
    segment_WF = song_WF[segment_starts[i]:segment_starts[i+1]]
    segment_WFs.append(segment_WF)

Segment.objects.create(
    segment_index=1,
    segment_list=segment_list,
    length_in_samples=3,
    start_position_in_samples=3,
    end_position_in_samples=6,
    WF=segment_WFs[0],
)

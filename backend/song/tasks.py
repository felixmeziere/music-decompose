"""
Celery tasks: functions runnable on separate async worker
"""
from celery import shared_task
from segmentation.models import Segmenter
from source_separation.models import SegmentGrouper, SourceExtractor
from song.models import Song

@shared_task
def run_full_flow(song_uuid):
    """
    Run full decomposition flow on selected songs
    """
    song = Song.objects.get(pk=song_uuid)
    song.segmenters.all().delete()
    song.async_process_and_save()
    segmenter = Segmenter.objects.create(
        parent=song,
        method='blind',
        tempo=song.tempo,
        n_tempo_lags_per_segment=4,
    )
    segmenter.async_process_and_save()
    segment_grouper = SegmentGrouper.objects.create(
        parent=segmenter,
        method='classic',
    )
    segment_grouper.async_process_and_save()
    source_extractor = SourceExtractor.objects.create(
        parent=segment_grouper,
        method='classic',
    )
    source_extractor.async_process_and_save()

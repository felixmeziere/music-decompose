"""
Celery tasks: functions runnable on separate async worker
"""
from celery import shared_task
from segmentation.models import Segmenter
from source_separation.models import SegmentGrouper, SourceExtractor
from song.models import Song, TempoEstimator

@shared_task
def run_full_flow(song_uuid):
    """
    Run full decomposition flow on selected songs
    """
    song = Song.objects.get(pk=song_uuid)
    song.tempo_estimators.all().delete()
    tempo_estimator = TempoEstimator.objects.create(
        parent=song,
        method='classic',
    )
    tempo_estimator.async_process_and_save(asynch=False)
    segmenter = Segmenter.objects.create(
        parent=tempo_estimator,
        method='blind',
        n_tempo_lags_per_segment=4,
    )
    segmenter.async_process_and_save(asynch=False)
    segment_grouper = SegmentGrouper.objects.create(
        parent=segmenter,
        method='classic',
    )
    segment_grouper.async_process_and_save(asynch=False)
    source_extractor = SourceExtractor.objects.create(
        parent=segment_grouper,
        method='classic',
    )
    source_extractor.async_process_and_save(asynch=False)

"""
Celery tasks: functions runnable on separate async worker
"""
from celery import shared_task


@shared_task
def run_full_flow_for_song(song_uuid):
    """
    Run full decomposition flow on selected songs
    """
    from segmentation.models import Segmenter
    from source_separation.models import SegmentGrouper, SourceExtractor
    from song.models import Song, TempoEstimator
    song = Song.objects.get(pk=song_uuid)
    song.import_song_WF()
    song.dump_data()
    song.tempo_estimators.all().delete()
    tempo_estimator = TempoEstimator.objects.create(
        parent=song,
        method='classic',
    )
    tempo_estimator.process_and_save(asynch=False)
    segmenter = Segmenter.objects.create(
        parent=tempo_estimator,
        method='blind',
        n_tempo_lags_per_segment=4,
    )
    segmenter.process_and_save(asynch=False)
    segment_grouper = SegmentGrouper.objects.create(
        parent=segmenter,
        method='classic',
    )
    segment_grouper.process_and_save(asynch=False)
    source_extractor = SourceExtractor.objects.create(
        parent=segment_grouper,
        method='classic',
    )
    source_extractor.process_and_save(asynch=False)

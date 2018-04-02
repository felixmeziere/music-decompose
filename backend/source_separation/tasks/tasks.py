"""
Celery tasks: used to run code asynchronously so that the web app can give immediate feedback
"""
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from music_decompose.services import do_task
from source_separation.models import SourceExtractor, SegmentGrouper
from .group_segments_for_segment_grouper import group_segments_for_segment_grouper
from .extract_sources_from_segment_groups_for_source_extractor import extract_sources_from_segment_groups_for_source_extractor

@shared_task
def asynch_group_segments_for_segment_grouper(segment_grouper_uuid):
    """
    group_segments_for_segment_grouper in the background
    """
    do_task(
        group_segments_for_segment_grouper,
        SegmentGrouper,
        segment_grouper_uuid,
    )

@shared_task
def asynch_extract_sources_from_segment_groups_for_source_extractor(source_extractor_uuid):
    """
    extract_sources_from_segment_groups_for_source_extractor in the background
    """
    do_task(
        extract_sources_from_segment_groups_for_source_extractor,
        SourceExtractor,
        source_extractor_uuid,
    )

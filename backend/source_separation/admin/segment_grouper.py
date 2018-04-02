"""
Admin for Segmenter model.
"""
from django.contrib import admin
from source_separation.tasks import asynch_group_segments_for_segment_grouper
from source_separation.models import SourceExtractor, SegmentGrouper
from source_separation.admin.source_extractor import SourceExtractorInline
from music_decompose.admin import ProcessorAdmin, ProcessorInline

def create_segment_groups(modeladmin, response, queryset): #pylint: disable=W0613
    """
    Action to create the segments groups for selected segment groupers
    """
    for segment_grouper in queryset:
        asynch_group_segments_for_segment_grouper.delay(segment_grouper.uuid)
create_segment_groups.short_description = 'Create Segment Groups'

def create_classic_source_extractor(modeladmin, response, queryset): #pylint: disable=W0613
    """
    Action to create a Source Extractor with method classic for this segment grouper
    """
    for segment_grouper in queryset:
        SourceExtractor.objects.create(
            parent=segment_grouper,
            method='classic',
        )
create_classic_source_extractor.short_description = 'Create Source Extractor with method classic'

class SegmentGrouperInline(ProcessorInline):
    """
    Segment Grouper Inline
    """
    model = SegmentGrouper


@admin.register(SegmentGrouper)
class SegmentGrouperAdmin(ProcessorAdmin):
    """
    Admin for SegmenterGrouper model.
    """
    actions = (create_segment_groups, create_classic_source_extractor,)
    inlines = (SourceExtractorInline,)

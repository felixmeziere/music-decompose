"""
Admin for Segmenter model.
"""
from django.contrib import admin
from segmentation.models import Segmenter
from segmentation.admin.segment import SegmentInline
from segmentation.tasks import asynch_compute_segmentation_for_segmenter
from source_separation.models import SegmentGrouper
from source_separation.admin import SegmentGrouperInline
from music_decompose.admin import ProcessorAdmin, ProcessorInline

def create_segments(modeladmin, response, queryset): #pylint: disable=W0613
    """
    Action to create the segments for selected songs
    """
    for segmenter in queryset:
        asynch_compute_segmentation_for_segmenter.delay(segmenter.uuid)
create_segments.short_description = 'Create Segments'

def create_classic_segment_grouper(modeladmin, response, queryset): #pylint: disable=W0613
    """
    Action to create a segment grouper with method classic for this segmenter
    """
    for segmenter in queryset:
        SegmentGrouper.objects.create(
            parent=segmenter,
            method='classic',
        )
create_classic_segment_grouper.short_description = 'Create Segment Grouper with method classic'


class SegmenterInline(ProcessorInline):
    """
    Segmenter Inline
    """
    model = Segmenter


@admin.register(Segmenter)
class SegmenterAdmin(ProcessorAdmin):
    """
    Admin for Segmenter model.
    """
    inlines = (SegmentGrouperInline, SegmentInline, )
    actions = (create_segments, create_classic_segment_grouper,)

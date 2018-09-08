"""
Admin for Segmenter model.
"""
from django.contrib import admin
from source_separation.models import SourceExtractor, SegmentGrouper
from source_separation.admin.source_extractor import SourceExtractorInline
from music_decompose.admin import ProcessorAdmin, ProcessorInline


def create_classic_source_extractor(modeladmin, response, queryset):  # pylint: disable=W0613
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
    actions = ProcessorAdmin.actions + (create_classic_source_extractor,)
    inlines = (SourceExtractorInline,)
    fields = ProcessorAdmin.fields + ('segment_groups',)
    readonly_fields = ProcessorAdmin.readonly_fields + ('segment_groups',)

"""
    Admin for Segmenter model.
"""
from django.contrib import admin
from source_separation.tasks import asynch_group_segments_for_segment_grouper
from source_separation.models import SourceExtractor, SegmentGrouper
from music_decompose.services import NoAddAdminMixin, get_link_to_modeladmin

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
            segment_grouper=segment_grouper,
            method='classic',
        )
create_classic_source_extractor.short_description = 'Create Source Extractor with method classic'

class SourceExtractorInline(NoAddAdminMixin, admin.TabularInline):
    """
    Source Separator Admin
    """
    model = SourceExtractor
    fields = (
        'method',
        'pretty_link',
    )
    readonly_fields = (
        'method',
        'pretty_link',
    )
    ordering = ('method',)
    show_change_link = True

    def pretty_link(self, obj): #pylint: disable=R0201
        """
        Displays nicely
        """
        return get_link_to_modeladmin(str(obj), 'source_separation', 'sourceextractor', obj.uuid)
    pretty_link.short_description = 'Link'


@admin.register(SegmentGrouper)
class SegmentGrouperAdmin(admin.ModelAdmin):
    """
        Admin for SegmenterGrouper model.
    """
    class Media:
        css = {
            'all': ('css/hide_admin_original.css', )     # Include extra css
        }
    ordering = ('segmenter', '-added_at',)
    actions = (create_segment_groups, create_classic_source_extractor,)
    inlines = (SourceExtractorInline,)
    fields = (
        'uuid',
        'added_at',
        'pretty_segmenter',
        'method',
        'segment_grouping_status',
        'segment_groups',
        'data_path',
    )
    readonly_fields = (
        'added_at',
        'uuid',
        'pretty_segmenter',
        'method',
        'segment_grouping_status',
        'segment_groups',
        'data_path',
    )
    list_display = (
        'uuid',
        'pretty_segmenter',
        'method',
        'segment_grouping_status',
    )

    def pretty_segmenter(self, obj): #pylint: disable=R0201
        """
        Segmenter object link
        """
        return get_link_to_modeladmin(str(obj.segmenter), 'segmentation', 'segmenter', obj.segmenter.uuid)
    pretty_segmenter.short_description = 'Segmenter'

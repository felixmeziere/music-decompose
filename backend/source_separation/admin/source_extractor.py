"""
Admin for SourceExtractor model.
"""
from django.contrib import admin
from source_separation.models import SourceExtractor, Source
from source_separation.tasks import asynch_extract_sources_from_segment_groups_for_source_extractor
from music_decompose.services import get_link_to_modeladmin
from music_decompose.services import audio_file_player, NoDeleteAdminMixin, NoAddAdminMixin

def create_sources(modeladmin, response, queryset): #pylint: disable=W0613
    """
    Action to create the sources for selected source extractors
    """
    for source_extractor in queryset:
        asynch_extract_sources_from_segment_groups_for_source_extractor.delay(source_extractor.uuid)
create_sources.short_description = 'Create Sources'

class SourceInline(NoDeleteAdminMixin, NoAddAdminMixin, admin.TabularInline):
    """
    Source Admin
    """
    model = Source
    fields = (
        'source_index',
        'segment_group',
        'audio_file',
        'audio_file_player',
    )
    readonly_fields = (
        'source_index',
        'segment_group',
        'audio_file',
        'audio_file_player',
    )

    def audio_file_player(self, obj): #pylint: disable=R0201
        """
            Audio player for segment file
        """
        return audio_file_player(obj.audio_file)

    ordering = ('source_index',)
    show_change_link = True


@admin.register(SourceExtractor)
class SourceExtractorAdmin(admin.ModelAdmin):
    """
        Admin for SourceExtractor model.
    """
    class Media:
        css = {
            'all': ('css/hide_admin_original.css', )     # Include extra css
        }
    ordering = ('segment_grouper', '-added_at',)
    inlines = (SourceInline,)
    actions = (create_sources,)
    fields = (
        'uuid',
        'added_at',
        'pretty_segment_grouper',
        'method',
        'source_separation_status',
        'data_path',
    )
    readonly_fields = (
        'added_at',
        'uuid',
        'pretty_segment_grouper',
        'method',
        'source_separation_status',
        'data_path',
    )
    list_display = (
        'uuid',
        'pretty_segment_grouper',
        'method',
        'source_separation_status',
    )

    def pretty_segment_grouper(self, obj): #pylint: disable=R0201
        """
        Segment Grouper object link
        """
        return get_link_to_modeladmin(str(obj.segment_grouper), 'source_separation', 'segmentgrouper', obj.segment_grouper.uuid)
    pretty_segment_grouper.short_description = 'Segment Grouper'

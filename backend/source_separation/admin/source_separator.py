"""
Admin for SourceSeparator model.
"""
from django.contrib import admin
from source_separation.models import SourceSeparator, Source
from source_separation.tasks import asynch_compute_source_separation_for_source_separator
from music_decompose.services import get_link_to_modeladmin
from music_decompose.services import audio_file_player, NoDeleteAdminMixin, NoAddAdminMixin

def create_sources(modeladmin, response, queryset): #pylint: disable=W0613
    """
    Action to create the sources for selected source separators
    """
    for source_separator in queryset:
        asynch_compute_source_separation_for_source_separator.delay(source_separator.uuid)
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


@admin.register(SourceSeparator)
class SourceSeparatorAdmin(admin.ModelAdmin):
    """
        Admin for SourceSeparator model.
    """
    class Media:
        css = {
            'all': ('css/hide_admin_original.css', )     # Include extra css
        }
    ordering = ('segmenter', '-added_at',)
    inlines = (SourceInline,)
    actions = (create_sources,)
    fields = (
        'uuid',
        'added_at',
        'pretty_segmenter',
        'method',
        'source_separation_status',
        'data_path',
    )
    readonly_fields = (
        'added_at',
        'uuid',
        'pretty_segmenter',
        'method',
        'source_separation_status',
        'data_path',
    )
    list_display = (
        'uuid',
        'pretty_segmenter',
        'method',
        'source_separation_status',
    )

    def pretty_segmenter(self, obj): #pylint: disable=R0201
        """
        Segmenter object link
        """
        return get_link_to_modeladmin(str(obj.segmenter), 'segmentation', 'segmenter', obj.segmenter.uuid)
    pretty_segmenter.short_description = 'Segmenter'

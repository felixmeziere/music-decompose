"""
    Admin for Song model.
"""
from django.contrib import admin
from segmentation.models import Segmenter, Segment
from segmentation.tasks import asynch_compute_segmentation_for_segmenter
from music_decompose.services import get_link_to_modeladmin
from music_decompose.services import audio_file_player, NoDeleteAdminMixin, NoAddAdminMixin

def create_segments(modeladmin, response, queryset): #pylint: disable=W0613
    """
    Action to create the segments for selected songs
    """
    for segmentList in queryset:
        asynch_compute_segmentation_for_segmenter.delay(segmentList.uuid)
create_segments.short_description = 'Create Segments'

class SegmentInline(NoDeleteAdminMixin, NoAddAdminMixin, admin.TabularInline):
    """
    Segment Admin
    """
    model = Segment
    fields = (
        'segment_index',
        'length_in_samples',
        'pretty_positions',
        'audio_file',
        'audio_file_player',
    )
    readonly_fields = (
        'segment_index',
        'length_in_samples',
        'pretty_positions',
        'audio_file',
        'audio_file_player',
    )

    def pretty_positions(self, obj): #pylint: disable=R0201
        """
        Displays nicely
        """
        return '[{0}, {1}['.format(str(obj.start_position_in_samples), str(obj.end_position_in_samples))

    def audio_file_player(self, obj): #pylint: disable=R0201
        """
            Audio player for segment file
        """
        return audio_file_player(obj.audio_file)

    pretty_positions.short_description = 'Limits in Samples'
    ordering = ('segment_index',)
    show_change_link = True


@admin.register(Segmenter)
class SegmenterAdmin(admin.ModelAdmin):
    """
        Admin for Song model.
    """
    class Media:
        css = {
            'all': ('css/hide_admin_original.css', )     # Include extra css
        }
    ordering = ('song', '-added_at',)
    inlines = (SegmentInline,)
    actions = (create_segments,)
    fields = (
        'uuid',
        'added_at',
        'pretty_song',
        'method',
        'n_tempo_lags_per_segment',
        'segmentation_status',
        'data_path',
    )
    readonly_fields = (
        'uuid',
        'added_at',
        'pretty_song',
        'method',
        'n_tempo_lags_per_segment',
        'segmentation_status',
        'data_path',
    )
    list_display = (
        'uuid',
        'pretty_song',
        'method',
        'n_tempo_lags_per_segment',
        'segmentation_status',
    )

    def pretty_song(self, obj): #pylint: disable=R0201
        """
        Song object link
        """
        return get_link_to_modeladmin(str(obj.song), 'song', 'song', obj.song.uuid)
    pretty_song.short_description = 'Song'

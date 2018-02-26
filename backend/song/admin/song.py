"""
    Admin for Song model.
"""
from django.contrib import admin
from song.models import Song
from segmentation.models import SegmentList
from music_decompose.services import audio_file_player, get_link_to_modeladmin, NoDeleteAdminMixin, NoAddAdminMixin

def estimate_tempo(modeladmin, response, queryset): #pylint: disable=W0613
    """
    Action to estimate tempo for song
    """
    for song in queryset:
        song.estimate_tempo()
estimate_tempo.short_description = 'Estimate Tempo'

def create_blind_segment_list(modeladmin, response, queryset): #pylint: disable=W0613
    """
    Action to start the segmentation of the song
    """
    for song in queryset:
        SegmentList.objects.create(
            song=song,
            method='blind',
        )
create_blind_segment_list.short_description = 'Create Segment List with method blind'

class SegmentListInline(NoDeleteAdminMixin, NoAddAdminMixin, admin.TabularInline):
    """
    Segment Admin
    """
    model = SegmentList
    fields = (
        'method',
        'n_tempo_lags_per_segment',
    )
    readonly_fields = (
        'method',
        'n_tempo_lags_per_segment',
    )
    ordering = ('method',)
    show_change_link = True


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    """
        Admin for Song model.
    """
    fields = (
        'uuid',
        'added_at',
        'title',
        'pretty_files',
        'tempo',
    )

    readonly_fields = (
        'uuid',
        'pretty_files',
        'added_at',
    )

    list_display = (
        'title',
        'pretty_files',
        'tempo',
    )

    actions = (estimate_tempo, create_blind_segment_list)

    list_display_links = ['title']

    def pretty_files(self, obj): #pylint: disable=R0201
        """
        Files object
        """
        return get_link_to_modeladmin('Go to files', 'song', 'songfiles', obj.files.uuid)
    pretty_files.short_description = 'Files'

    ordering = ('-added_at',)
    inlines = (SegmentListInline,)

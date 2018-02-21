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

class SegmentListInline(NoDeleteAdminMixin, NoAddAdminMixin, admin.TabularInline):
    """
    Segment Admin
    """
    model = SegmentList
    fields = (
        'method',
    )
    readonly_fields = (
        'method',
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

    actions = (estimate_tempo,)

    list_display_links = ['title']

    def pretty_files(self, obj): #pylint: disable=R0201
        """
        Files object
        """
        return get_link_to_modeladmin('Go to files', 'song', 'songfiles', obj.files.uuid)
    pretty_files.short_description = 'Files'

    ordering = ('-added_at',)
    inlines = (SegmentListInline,)

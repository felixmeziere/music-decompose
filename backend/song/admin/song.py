"""
Admin for Song model.
"""
from django.contrib import admin
from song.models import Song, TempoEstimator
from song.admin.tempo_estimator import TempoEstimatorInline
from music_decompose.services import audio_file_player

def run_full_flow_for_songs(modeladmin, response, queryset): #pylint: disable=W0613
    """
    Run full decomposition flow on selected songs
    """
    for song in queryset:
        song.run_full_flow()

def create_classic_tempo_estimator(modeladmin, response, queryset): #pylint: disable=W0613
    """
    Action to create tempo estimator with method classic for this song
    """
    for song in queryset:
        TempoEstimator.objects.create(
            parent=song,
            method='classic',
        )
create_classic_tempo_estimator.short_description = 'Create Tempo Estimator with method classic'

@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    """
    Admin for Song model.
    """
    fields = (
        'uuid',
        'added_at',
        'title',
        'original_file',
        'original_song_player',
    )

    readonly_fields = (
        'uuid',
        'original_file',
        'added_at',
        'original_song_player',
        'title',
    )

    list_display = (
        'title',
        'original_file',
        'original_song_player',
    )

    actions = (create_classic_tempo_estimator, run_full_flow_for_songs)

    list_display_links = ['title']

    def original_song_player(self, obj): #pylint: disable=R0201
        """
        Audio player for original file
        """
        return audio_file_player(obj.original_file)
    original_song_player.allow_tags = True
    original_song_player.short_description = ('Original song player')


    ordering = ('-added_at',)
    inlines = (TempoEstimatorInline,)

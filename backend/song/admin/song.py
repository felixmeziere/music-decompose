"""
Admin for Song model.
"""
from django.contrib import admin
from song.models import Song
from song.tasks import asynch_compute_tempo_for_song
from segmentation.models import Segmenter
from segmentation.admin import SegmenterInline
from music_decompose.services import audio_file_player

def compute_tempo(modeladmin, response, queryset): #pylint: disable=W0613
    """
    Action to estimate tempo for song
    """
    for song in queryset:
        asynch_compute_tempo_for_song.delay(song.uuid)
compute_tempo.short_description = 'Estimate Tempo'

def create_blind_segmenter(modeladmin, response, queryset): #pylint: disable=W0613
    """
    Action to create segmenter with method blind for this song
    """
    for song in queryset:
        if song.tempo:
            Segmenter.objects.create(
                parent=song,
                method='blind',
                tempo=song.tempo,
                n_tempo_lags_per_segment=4,
            )
        else:
            raise Exception('Please compute the tempo of the song before segmenting it.')
create_blind_segmenter.short_description = 'Create Segmenter with method blind'

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
        'processing_status',
        'tempo',
    )

    readonly_fields = (
        'uuid',
        'original_file',
        'added_at',
        'original_song_player',
        'title',
        'processing_status',
    )

    list_display = (
        'title',
        'original_file',
        'processing_status',
        'tempo',
        'original_song_player',
    )

    actions = (compute_tempo, create_blind_segmenter)

    list_display_links = ['title']

    def original_song_player(self, obj): #pylint: disable=R0201
        """
        Audio player for original file
        """
        return audio_file_player(obj.original_file)
    original_song_player.allow_tags = True
    original_song_player.short_description = ('Original song player')


    ordering = ('-added_at',)
    inlines = (SegmenterInline,)

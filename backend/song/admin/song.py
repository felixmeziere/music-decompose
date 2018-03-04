"""
    Admin for Song model.
"""
from django.contrib import admin
from song.models import Song
from song.tasks import asynch_compute_tempo_for_song
from segmentation.models import Segmenter
from music_decompose.services import audio_file_player, NoAddAdminMixin

def compute_tempo(modeladmin, response, queryset): #pylint: disable=W0613
    """
    Action to estimate tempo for song
    """
    for song in queryset:
        asynch_compute_tempo_for_song.delay(song.uuid)
compute_tempo.short_description = 'Estimate Tempo'

def create_blind_segmenter(modeladmin, response, queryset): #pylint: disable=W0613
    """
    Action to start the segmentation of the song
    """
    for song in queryset:
        if song.tempo:
            Segmenter.objects.create(
                song=song,
                method='blind',
                tempo=song.tempo,
                n_tempo_lags_per_segment=4,
            )
        else:
            raise Exception('Please compute the tempo of the song before segmenting it.')
create_blind_segmenter.short_description = 'Create Segmenter with method blind'

class SegmenterInline(NoAddAdminMixin, admin.TabularInline):
    """
    Segment Admin
    """
    model = Segmenter
    fields = (
        'method',
        'tempo',
        'n_tempo_lags_per_segment',
    )
    readonly_fields = (
        'method',
        'tempo',
        'n_tempo_lags_per_segment',
    )
    ordering = ('method', 'tempo', 'n_tempo_lags_per_segment')
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
        'original_file',
        'original_song_player',
        'tempo_estimation_status',
        'tempo',
    )

    readonly_fields = (
        'uuid',
        'original_file',
        'added_at',
        'original_song_player',
        'title',
        'tempo_estimation_status',
    )

    list_display = (
        'title',
        'original_file',
        'tempo_estimation_status',
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

"""
    Admin for Song model.
"""
from django.contrib import admin
from segmentation.models import SegmentList, Segment
from music_decompose.services import get_link_to_modeladmin
from music_decompose.services import audio_file_player, NoDeleteAdminMixin, NoAddAdminMixin

class SegmentInline(NoDeleteAdminMixin, NoAddAdminMixin, admin.TabularInline):
    """
    Segment Admin
    """
    model = Segment
    fields = (
        'index',
        'length_in_samples',
        'pretty_positions',
        'audio_file',
        'audio_file_player',
    )
    readonly_fields = (
        'index',
        'length_in_samples',
        'pretty_positions',
        'audio_file',
        'audio_file_player',
    )

    def pretty_positions(self, obj):
        """
        Displays nicely
        """
        return [obj.start_position_in_samples, obj.end_position_in_samples]

    def audio_file_player(self, obj): #pylint: disable=R0201
        """
            Audio player for segment file
        """
        return audio_file_player(obj.audio_file)

    pretty_positions.short_description = 'Limits in Samples'
    ordering = ('index',)
    show_change_link = True


@admin.register(SegmentList)
class SegmentListAdmin(admin.ModelAdmin):
    """
        Admin for Song model.
    """
    class Media:
        css = {
            'all': ('css/hide_admin_original.css', )     # Include extra css
        }
    fields = (
        'uuid',
        'added_at',
        'pretty_song',
        'method',
    )

    readonly_fields = (
        'uuid',
        'added_at',
        'pretty_song',
        'method',
    )

    list_display = (
        'uuid',
        'pretty_song',
        'method',
    )

    def pretty_song(self, obj): #pylint: disable=R0201
        """
        Song object link
        """
        return get_link_to_modeladmin(str(obj.song), 'song', 'song', obj.song.uuid)
    pretty_song.short_description = 'Song'

    ordering = ('song', '-added_at',)

    inlines = (SegmentInline,)

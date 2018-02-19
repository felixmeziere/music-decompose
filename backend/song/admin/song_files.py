"""
    Admin for Song model.
"""
import os
from django.contrib import admin
from song.models import SongFiles
from music_decompose.services import audio_file_player, get_link_to_modeladmin

@admin.register(SongFiles)
class SongFilesAdmin(admin.ModelAdmin):
    """
        Admin for Song Files model.
    """
    fields = (
        '__str__',
        'uuid',
        'added_at',
        'original_file',
        'pretty_song',
        'original_file_player',
    )

    readonly_fields = (
        '__str__',
        'added_at',
        'original_file',
        'pretty_song',
        'uuid',
        'original_file_player',
    )

    list_display = (
        '__str__',
        'pretty_song',
        'original_file',
        'original_file_player',
    )
    actions = ['custom_delete_selected']

    list_display_links = ['__str__']

    ordering = ('song', '-added_at',)

    def get_actions(self, request):
        """
        Override
        """
        actions = super(SongFilesAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def custom_delete_selected(self, request, queryset):
        """
        Make sure file deleted from the file system as well.
        """
        #custom delete code
        number = queryset.count()
        for i in queryset:
            if i.original_file:
                if os.path.exists(i.original_file.path):
                    os.remove(i.original_file.path)
            i.delete()
        self.message_user(request, ('Successfully deleted %d audio files.') % number)
    custom_delete_selected.short_description = 'Delete selected items'

    def pretty_song(self, obj): #pylint: disable=R0201
        """
        Link to song object
        """
        return get_link_to_modeladmin(str(obj.song), 'song', 'song', obj.song.uuid)
    pretty_song.short_description = 'Song'

    def original_file_player(self, obj): #pylint: disable=R0201
        """
            Audio player for original file
        """
        return audio_file_player(obj.original_file)

    original_file_player.allow_tags = True
    original_file_player.short_description = ('Original file player')

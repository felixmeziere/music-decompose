"""
    Admin for Song model.
"""
import os
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from song.models import SongFiles

@admin.register(SongFiles)
class SongFilesAdmin(admin.ModelAdmin):
    """
        Admin for Song Files model.
    """
    fields = (
        '__str__',
        'uuid',
        'original_file',
        'added_at',
        'pretty_song',
        'audio_file_player',
    )

    readonly_fields = (
        '__str__',
        'added_at',
        'original_file',
        'pretty_song',
        'uuid',
        'audio_file_player',
    )

    list_display = (
        '__str__',
        'pretty_song',
        'original_file',
        'audio_file_player',
        'added_at',
    )
    actions = ['custom_delete_selected']

    list_display_links = ['__str__']

    ordering = ('-added_at',)

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
        return format_html(
            "<a href='{url}'>" + str(obj.song) + "</a>",
            url=reverse('admin:song_song_change',
                        args=(obj.song.uuid if obj.song else None,))
        )
    pretty_song.short_description = 'Song'

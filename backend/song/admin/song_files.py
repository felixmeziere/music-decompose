"""
    Admin for Song model.
"""
import os
from django.contrib import admin
from django.urls import reverse
from song.models import SongFiles
from django.utils.html import format_html

@admin.register(SongFiles)
class SongFilesAdmin(admin.ModelAdmin):
    """
        Admin for Song Files model.
    """
    fields = (
        'uuid',
        'original_file',
        'added_at',
        'pretty_song',
        'audio_file_player',
    )

    readonly_fields = (
        'uuid',
        'added_at',
        'original_file',
        'pretty_song',
        'audio_file_player',
    )

    list_display = (
        'pretty_song',
        'original_file',
        'audio_file_player',
        'added_at',
    )
    actions = ['custom_delete_selected']

    ordering = ('-added_at',)

    def get_actions(self, request):
        actions = super(SongFilesAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def custom_delete_selected(self, request, queryset):
        #custom delete code
        n = queryset.count()
        for i in queryset:
            if i.original_file:
                if os.path.exists(i.original_file.path):
                    os.remove(i.original_file.path)
            i.delete()
        self.message_user(request, ('Successfully deleted %d audio files.') % n)
    custom_delete_selected.short_description = 'Delete selected items'

    def pretty_song(self, obj):
        return format_html("<a href='{url}'>" + str(obj.song) + "</a>", url=reverse('admin:song_song_change', args=(obj.song.uuid if obj.song else None,)))
    pretty_song.short_description = 'Song'

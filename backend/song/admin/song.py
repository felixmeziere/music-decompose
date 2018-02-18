"""
    Admin for Song model.
"""
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from song.models import Song


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
    )

    readonly_fields = (
        'pretty_files',
        'added_at',
    )

    list_display = (
        'title',
        'pretty_files',
        'added_at',
    )

    list_display_links = ['title']

    def pretty_files(self, obj): #pylint: disable=R0201
        """
        Files object
        """
        return format_html(
            "<a href='{url}'>Go to files</a>",
            url=reverse('admin:song_songfiles_change',
                        args=(obj.files.uuid,))
        )
    pretty_files.short_description = 'Files'

    ordering = ('-added_at',)

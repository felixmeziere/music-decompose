"""
    Admin for Song model.
"""
from django.contrib import admin
from vehicle.models import Song

@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    """
        Admin for Song model.
    """
    fields = (
        'uuid',
        'added_at',
    )


    readonly_fields = (
        'uuid',
        'added_at',
    )

    list_display = (
        'uuid',
        'added_at',
    )

    ordering = ('-added_at',)

"""
Admin for Container Abstract model.
"""
from django.contrib import admin
from music_decompose.services import get_link_to_modeladmin
from music_decompose.services import NoDeleteAdminMixin, NoAddAdminMixin


# @admin.register(Container)
class ContainerAdmin(admin.ModelAdmin):
    """
    Admin for Container Abstract model.
    """
    ordering = (
        'parent',
        '-added_at',
    )
    fields = (
        'uuid',
        'added_at',
        'pretty_song',
        'processing_status',
        'data_path',
    )
    readonly_fields = (
        'uuid',
        'added_at',
        'pretty_song',
        'processing_status',
        'data_path',
    )
    list_display = (
        'uuid',
        'pretty_song',
        'processing_status',
    )
    actions = ()

    def pretty_song(self, obj):    #pylint: disable=R0201
        """
        Song object link
        """
        return get_link_to_modeladmin(str(obj.song), 'song_song', obj.song.uuid)

    pretty_song.short_description = 'Song'

    def pretty_parent_container(self, obj):    #pylint: disable=R0201
        """
        Parent Container object link
        """
        if not obj.parent:
            return 'No Parent'
        return get_link_to_modeladmin(str(obj.parent), obj.parent._meta.db_table, obj.parent.uuid)

    pretty_parent_container.short_description = 'Parent Container'


class ContainerInline(NoDeleteAdminMixin, NoAddAdminMixin, admin.TabularInline):
    """
    Inline for Abstract Class Container
    """
    model = None
    fields = ()
    readonly_fields = ()
    ordering = ()
    show_change_link = True

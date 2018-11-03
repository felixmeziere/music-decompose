"""
Admin for Ouptut submodel.
"""
from music_decompose.admin.container import ContainerInline
from music_decompose.services import audio_file_player


class OutputInline(ContainerInline):
    """
    Inline for Abstract Class Output
    """
    fields = ContainerInline.fields + (
        'ind',
        'audio_file',
        'audio_file_player',
    )
    readonly_fields = ContainerInline.fields + (
        'ind',
        'audio_file',
        'audio_file_player',
    )

    ordering = ('ind', )
    show_change_link = True

    def audio_file_player(self, obj):    #pylint: disable=R0201
        """
        Audio player for output file
        """
        return audio_file_player(obj.audio_file)

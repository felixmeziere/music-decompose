"""
Admin for Source model.
"""
from source_separation.models import Source
from music_decompose.admin import OutputInline


class SourceInline(OutputInline):
    """
    Source Inline
    """
    model = Source
    fields = OutputInline.fields + (
        'segment_group',
    )
    readonly_fields = OutputInline.readonly_fields + (
        'segment_group',
    )

"""
Admin for Segment model
"""

from segmentation.models import Segment
from music_decompose.admin import OutputInline


class SegmentInline(OutputInline):
    """
    Segment Admin
    """
    model = Segment
    fields = OutputInline.fields + (
        'length_in_samples',
        'pretty_positions',
    )
    readonly_fields = OutputInline.readonly_fields + (
        'length_in_samples',
        'pretty_positions',
    )

    def pretty_positions(self, obj): #pylint: disable=R0201
        """
        Displays nicely
        """
        return '[{0}, {1}['.format(str(obj.start_position_in_samples), str(obj.end_position_in_samples))
    pretty_positions.short_description = 'Limits in Samples'

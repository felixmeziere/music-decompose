"""
Admin for SegmentGroup model
"""

from source_separation.models import SegmentGroup
from music_decompose.admin import OutputInline


class SegmentGroupInline(OutputInline):
    """
    SegmentGroup Admin
    """
    model = SegmentGroup
    fields = OutputInline.fields + ('segment_group', )
    readonly_fields = OutputInline.readonly_fields + ('segment_group', )

    # def pretty_positions(self, obj):    #pylint: disable=R0201
    #     """
    #     Displays nicely
    #     """
    #     return '[{0}, {1}['.format(str(obj.start_position_in_samples), str(obj.end_position_in_samples))

    # pretty_positions.short_description = 'Limits in Samples'

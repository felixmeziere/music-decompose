"""
compute_source_separation from SourceSeparator data and store results in SourceSeparator.
"""

from source_separation.sp_functions import compute_source_separation
from source_separation.models import SourceSeparator

def compute_source_separation_for_source_separator(source_separator_uuid):
    """
    The function
    """
    ### Initialise
    source_separator = SourceSeparator.objects.get(pk=source_separator_uuid)
    source_separator.source_separation_status = 'pending'
    source_separator.save()

    try:
        ### Detect segment limits
        segment_groups = compute_source_separation(
            source_separator.method,
            source_separator.segmenter.segment_WF,
        )

        ### Save data
        source_separator._segment_groups = segment_groups
        source_separator.create_source_WFs() # WRITE THIS FUNCTION HERE
        source_separator.create_sources() # WRITE THIS FUNCTION HERE
        source_separator.dump_data()
        source_separator.save()

        ### End
        source_separator.source_separation_status = 'done'
        source_separator.save()
    except Exception as error:
        source_separator.source_separation_status = 'failed'
        source_separator.save()
        raise error

"""
Admin for SourceExtractor model.
"""
from django.contrib import admin
from source_separation.models import SourceExtractor
from source_separation.tasks import asynch_extract_sources_from_segment_groups_for_source_extractor
from source_separation.admin.source import SourceInline
from music_decompose.admin import ProcessorAdmin, ProcessorInline

def create_sources(modeladmin, response, queryset): #pylint: disable=W0613
    """
    Action to create the sources for selected source extractors
    """
    for source_extractor in queryset:
        asynch_extract_sources_from_segment_groups_for_source_extractor.delay(source_extractor.uuid)
create_sources.short_description = 'Create Sources'

class SourceExtractorInline(ProcessorInline):
    """
    Source Extractor Inline
    """
    model = SourceExtractor


@admin.register(SourceExtractor)
class SourceExtractorAdmin(ProcessorAdmin):
    """
    Admin for SourceExtractor model.
    """
    inlines = (SourceInline,)
    actions = (create_sources,)

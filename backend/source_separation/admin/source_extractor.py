"""
Admin for SourceExtractor model.
"""
from django.contrib import admin
from source_separation.models import SourceExtractor
from source_separation.admin.source import SourceInline
from music_decompose.admin import ProcessorAdmin, ProcessorInline


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
    inlines = (SourceInline, )
    actions = ProcessorAdmin.actions + ()

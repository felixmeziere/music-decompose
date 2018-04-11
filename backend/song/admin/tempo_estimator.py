"""
Admin for Segmenter model.
"""
from django.contrib import admin
from song.models import TempoEstimator
from music_decompose.admin import ProcessorAdmin, ProcessorInline
from segmentation.models import Segmenter
from segmentation.admin import SegmenterInline

def compute_tempo(modeladmin, response, queryset): #pylint: disable=W0613
    """
    Action to estimate tempo for song
    """
    for tempo_estimator in queryset:
        tempo_estimator.async_process_and_save()
compute_tempo.short_description = 'Estimate Tempo'

def create_blind_segmenter(modeladmin, response, queryset): #pylint: disable=W0613
    """
    Action to create segmenter with method blind for this tempo estimator
    """
    for tempo_estimator in queryset:
        Segmenter.objects.create(
            parent=tempo_estimator,
            method='blind',
            n_tempo_lags_per_segment=4,
        )
create_blind_segmenter.short_description = 'Create Segmenter with method blind'

class TempoEstimatorInline(ProcessorInline):
    """
    Tempo Estimator Inline
    """
    model = TempoEstimator


@admin.register(TempoEstimator)
class TempoEstimatorAdmin(ProcessorAdmin):
    """
    Admin for TempoEstimator model.
    """
    actions = ProcessorAdmin.actions + (compute_tempo, create_blind_segmenter,)
    inlines = (SegmenterInline,)
    fields = ProcessorAdmin.fields + ('tempo',)
    list_display = ProcessorAdmin.list_display + ('tempo',)

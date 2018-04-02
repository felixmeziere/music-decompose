"""
Actions to execute before Django starts. Used mainly to add fields to existing
classes dynamically.
"""

from django.contrib import admin
from music_decompose.models.make_class import make_processor
from music_decompose.admin.make_admin import make_processor_admin, make_processor_inline

from music_decompose.models import Processor
from music_decompose.admin import ProcessorAdmin, ProcessorInline

for model in Processor.__subclasses__():
    make_processor(model)

for inline in ProcessorInline.__subclasses__():
    make_processor_inline(inline.model, inline)

for model in admin.site._registry:
    model_admin = admin.site._registry[model].__class__
    if issubclass(model_admin, ProcessorAdmin):
        make_processor_admin(model, model_admin)

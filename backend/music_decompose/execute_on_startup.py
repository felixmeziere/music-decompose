"""
Actions to execute before Django starts. Used mainly to add fields to existing
classes dynamically.
"""

from django.contrib import admin
from music_decompose.models.make_class import make_container
from music_decompose.admin.make_admin import make_processor_admin, make_processor_inline
from music_decompose.services import get_leaf_submodels
from music_decompose.models import Container
from music_decompose.admin import ProcessorAdmin, ProcessorInline


for model in get_leaf_submodels(Container):
    make_container(model)

for inline in get_leaf_submodels(ProcessorInline):
    make_processor_inline(inline.model, inline)

for model in admin.site._registry:
    model_admin = admin.site._registry[model].__class__
    if issubclass(model_admin, ProcessorAdmin):
        make_processor_admin(model, model_admin)

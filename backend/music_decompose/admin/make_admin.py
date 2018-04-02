"""
Add dynamic attributes to Abstract admin models
"""
from .processor import ProcessorAdmin, ProcessorInline

def make_processor_admin(ProcessorSubClass, ProcessorAdminSubClass):
    """
    Add attributes to Processor Admin based on parameters
    """
    ProcessorAdminSubClass.fields = ProcessorAdmin.fields + ProcessorSubClass.parameters
    ProcessorAdminSubClass.readonly_fields = ProcessorAdmin.readonly_fields + ProcessorSubClass.parameters
    ProcessorAdminSubClass.list_display = ProcessorAdmin.list_display + ProcessorSubClass.parameters
    ProcessorAdminSubClass.ordering = ProcessorAdmin.ordering + ProcessorSubClass.parameters

def make_processor_inline(ProcessorSubClass, ProcessorInlineSubClass):
    """
    Add attributes to Processor Inline based on parameters
    """
    ProcessorInlineSubClass.fields = ProcessorInline.fields + ProcessorSubClass.parameters
    ProcessorInlineSubClass.readonly_fields = ProcessorInline.readonly_fields + ProcessorSubClass.parameters
    ProcessorInlineSubClass.ordering = ProcessorInline.ordering + ProcessorSubClass.parameters

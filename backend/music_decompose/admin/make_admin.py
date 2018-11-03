"""
Add dynamic attributes to Abstract admin models
"""


def make_processor_admin(ProcessorSubClass, ProcessorAdminSubClass):
    """
    Add attributes to Processor Admin based on parameters
    """
    ProcessorAdminSubClass.fields += ProcessorSubClass.parameters
    ProcessorAdminSubClass.readonly_fields += ProcessorSubClass.parameters
    ProcessorAdminSubClass.list_display += ProcessorSubClass.parameters
    ProcessorAdminSubClass.ordering += ProcessorSubClass.parameters


def make_processor_inline(ProcessorSubClass, ProcessorInlineSubClass):
    """
    Add attributes to Processor Inline based on parameters
    """
    ProcessorInlineSubClass.fields += ProcessorSubClass.parameters
    ProcessorInlineSubClass.readonly_fields += ProcessorSubClass.parameters
    ProcessorInlineSubClass.ordering += ProcessorSubClass.parameters

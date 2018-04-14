"""
Admin for Processor Submodel.
"""
from music_decompose.admin.container import ContainerAdmin, ContainerInline
from music_decompose.services import get_link_to_modeladmin

class ProcessorInline(ContainerInline):
    """
    Inline for Abstract Class Processor
    """
    fields = ContainerInline.fields + (
        'pretty_link',
    )
    readonly_fields = ContainerInline.fields + (
        'pretty_link',
    )

    def pretty_link(self, obj): #pylint: disable=R0201
        """
        Displays nicely
        """
        return get_link_to_modeladmin(str(obj), obj._meta.db_table, obj.uuid)
    pretty_link.short_description = 'Link'

def _process_and_save(modeladmin, response, queryset): #pylint: disable=W0613
    """
    Action to run _process_and_save asynchronously on selected objects
    """
    for instance in queryset:
        instance.process_and_save()

class ProcessorAdmin(ContainerAdmin):
    """
    Admin for Processor Abstract model.
    """
    class Media:
        """
        Django Media class
        """
        css = {
            'all': ('css/hide_admin_original.css', )     # Include extra css
        }
    fields = ContainerAdmin.fields + ()
    readonly_fields = ContainerAdmin.readonly_fields + ()
    list_display = ContainerAdmin.list_display + ()
    ordering = ContainerAdmin.ordering + ()
    actions = ContainerAdmin.actions + (_process_and_save,)

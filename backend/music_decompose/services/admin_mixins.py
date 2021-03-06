"""
Mixins to disallow access rights to admin
"""


class NoDeleteAdminMixin():
    """
    Disallow delete.
    """

    @staticmethod
    def has_delete_permission(*args, **kwargs):    # pylint: disable=unused-argument
        """Gets delete persission for object page.
        :returns: False
        """
        return False

    def get_actions(self, request):
        """Removes the default delete action.
        :returns: actions exlcuding default delete action
        """
        # source: http://stackoverflow.com/a/34152539
        actions = super(NoDeleteAdminMixin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        assert not any('delete' in action_name for action_name in actions)
        return actions


class NoAddAdminMixin():
    """
    Disallow Add.
    """

    @staticmethod
    def has_add_permission(*args):    # pylint: disable=unused-argument
        """
        Gets add permission for object page.
        :returns: False
        """
        return False


class ReadOnlyViewAdminMixin():
    """
    Disallow change by making all fields readonly. Allow view.
    """

    def get_readonly_fields(self, request, obj=None):    # pylint: disable=unused-argument
        """
        Get fields to show on object page.
        :returns: list of field names
        """
        return self.fields

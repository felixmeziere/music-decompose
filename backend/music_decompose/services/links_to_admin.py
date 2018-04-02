"""
Return link to change view of a model object in the admin.
"""
from django.utils.html import format_html
from django.urls import reverse

def get_link_to_modeladmin(text, table, primary_key):
    """
    Return link to change view of a model object in the admin.
    """
    return format_html(
        "<a href='{url}'>" + text + "</a>",
        url=reverse('admin:{0}_change'.format(table),
                    args=(primary_key,))
    )

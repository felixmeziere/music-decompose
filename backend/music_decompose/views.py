"""
Core Views that serves the endpoints like the frontend
"""

from django.conf import settings
from django.shortcuts import render
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.views.generic.base import RedirectView

def app(request):
    """
    Endpoint to serve the React App
    """
    if settings.CUSTOM_BUNDLE_URL:  # Dev only
        bundle_url = settings.CUSTOM_BUNDLE_URL
    else:
        bundle_url = static('bundle.js')

    response = render(request, 'index.html', {
        'bundleUrl': bundle_url,
    })

    return response


def frontend_static_redirect(request, rest_of_path=''):
    """
    Static redirect into the /frontend-static/ folder
    """
    return RedirectView.as_view(url='http://localhost:3000/frontend-static/' + rest_of_path, permanent=True)(request)

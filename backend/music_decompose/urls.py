"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from rest_framework import routers
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from music_decompose import views
from song.views import AddSongViewSet

ROUTER = routers.DefaultRouter()
ROUTER.register(r'song', AddSongViewSet)

urlpatterns = [ #pylint: disable=C0103
    # Architecture
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^$', views.app, name='app'),
    url(
        r'^frontend-static/(?P<rest_of_path>.*)',
        views.frontend_static_redirect,
        name='frontend-static-files'
    ),
    url(r'^sockjs-node/(?P<rest_of_path>.*)', views.sockjs_node_redirect, name='sockjs-node'),
    # Features
    url(r'^', include(ROUTER.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

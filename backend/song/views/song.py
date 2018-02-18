# -*- coding: utf-8 -*-
"""
Views for the Songs
"""
from rest_framework import viewsets, mixins
from song.models import Song
from song.serializers import SongSerializer

class SongViewSet(mixins.CreateModelMixin,
                  viewsets.GenericViewSet):
    """
        Song metadata management endpoint
    """
    queryset = Song.objects.all()
    serializer_class = SongSerializer

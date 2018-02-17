# -*- coding: utf-8 -*-
"""
Views for the Songs
"""
from song.models import Song
from song.serializers import SongSerializer
from rest_framework import viewsets, mixins
class AddSongViewSet(mixins.CreateModelMixin,
                     viewsets.GenericViewSet):
    """
        Song metadata management endpoint
    """
    queryset = Song.objects.all()
    serializer_class = SongSerializer

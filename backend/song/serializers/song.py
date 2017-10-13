"""
    Serializes a song
"""
from rest_framework import serializers
from song.models import Song


class SongSerializer(serializers.ModelSerializer):
    """
        Serializer of the Song model
    """
    class Meta:
        """
            Django Meta class
        """
        model = Song
        fields = (
            'uuid',
        )

    def create(self, validated_data):
        print('TOTOR')
        return super(SongSerializer, self).create(validated_data)

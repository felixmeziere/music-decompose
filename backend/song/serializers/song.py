"""
    Serializes song metadata
"""
from rest_framework import serializers
from song.models import Song
from .song_files import SongFilesSerializer


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
            'added_at',
            'files',
            'title',
        )

        read_only_fields = (
            'uuid',
            'added_at',
        )

    files = SongFilesSerializer(partial=True, required=False)

    def create(self, validated_data):
        file_data = self.initial_data['file']
        instance = super(SongSerializer, self).create(validated_data)

        if file_data is not None:
            data = {
                'file': file_data,
                'song': instance,
            }
            serializer = SongFilesSerializer(data=data)
            serializer.is_valid()
            serializer.create(data)

        return instance

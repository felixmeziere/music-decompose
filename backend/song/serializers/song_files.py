"""
    Serializes song file upload and management
"""
from rest_framework import serializers
from song.models import SongFiles


class SongFilesSerializer(serializers.ModelSerializer):
    """
        Serializer of the SongFiles model.
    """

    file = serializers.FileField(source='original_file')

    class Meta:
        """
            Django Meta class
        """
        model = SongFiles
        fields = (
            'uuid',
            'added_at',
            'file',
            'song',
        )

        read_only_fields = (
            'uuid',
            'added_at',
        )


    def create(self, validated_data):
        file_data = validated_data.pop('file')
        instance = super(SongFilesSerializer, self).create(validated_data)

        if file_data is not None:
            instance.original_file = file_data
            instance.save()
        return instance

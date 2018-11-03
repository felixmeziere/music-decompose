"""
Serializes song metadata and original audio file
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
            'added_at',
            'original_file',
            'title',
        )

        read_only_fields = (
            'uuid',
            'added_at',
        )

    def create(self, validated_data):
        """
        Customise create to dump song waveform to file
        """
        instance = super(SongSerializer, self).create(validated_data)
        try:
            instance.import_song_WF()
            instance.dump_data()
            instance.save()
            return instance
        except Exception as error:
            instance.delete()
            raise serializers.ValidationError('The song WF couldn\'t be handled: {}'.format(error))

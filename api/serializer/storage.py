from rest_framework import serializers
from django.utils.translation import gettext as _
from rest_framework.fields import empty

from db.models import LocalStorage
from utils.tasks import add_watermark
import filetype


class LocalStorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocalStorage
        fields = ('file', )

    def __init__(self, instance=None, data=empty, **kwargs):
        self._user = self.partial = kwargs.pop('user', None)
        super().__init__(instance=instance, data=data, **kwargs)

    def validate_file(self, value):
        kind = filetype.guess(value)
        if kind is None:
            raise serializers.ValidationError(_('unsupported file type'))
        if value.content_type != kind.mime:
            value.content_type = kind.mime
        return value

    def create(self, validated_data):
        file_type = validated_data['file'].content_type
        storage = LocalStorage.objects.create(user=self._user, type=file_type, file=validated_data['file'])

        if file_type.startswith('image') or file_type.startswith('video'):
            add_watermark.delay(storage.id)

        if file_type.startswith('audio'):
            from pydub import AudioSegment
            audio = AudioSegment.from_file(storage.file.path)
            storage.duration_seconds = audio.duration_seconds
            storage.save()
        return storage

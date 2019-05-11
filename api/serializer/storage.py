from rest_framework import serializers
from django.utils.translation import gettext as _
from rest_framework.fields import empty

from db.models import LocalStorage


class LocalStorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocalStorage
        fields = ('file', )

    def __init__(self, instance=None, data=empty, **kwargs):
        self._user = self.partial = kwargs.pop('user', None)
        super().__init__(instance=instance, data=data, **kwargs)

    def create(self, validated_data):
        file_type = validated_data['file'].content_type
        return LocalStorage.objects.create(user=self._user, type=file_type, file=validated_data['file'])


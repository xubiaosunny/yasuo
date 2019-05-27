from rest_framework import serializers
from django.utils.translation import gettext as _
from db.models import Works


class WorksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Works
        fields = ('type', 'storage', 'summary', 'location')

    def validate_storage(self, value):
        if not value.type.startswith('image') and not value.type.startswith('video'):
            raise serializers.ValidationError(_('The file type is incorrect, Please upload an image or video'))
        return value

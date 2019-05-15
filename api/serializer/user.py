from rest_framework import serializers
from django.utils.translation import gettext as _
from db.models import CustomUser, LocalStorage


class UserInfoSerializer(serializers.ModelSerializer):
    id_number = serializers.CharField(required=False, help_text=_('ID Number'))
    certified_file = serializers.IntegerField(required=False, help_text=_('Certified File'))

    class Meta:
        model = CustomUser
        fields = ('full_name', 'province', 'city', 'role', 'grade', 'work_place', 'id_number', 'certified_file')

    def validate_certified_file(self, value):
        if not value:
            return value
        if self.data.get('role', None) != CustomUser.ROLE_CHOICES[0][0]:
            return value
        try:
            stroge = LocalStorage.objects.get(pk=value)
        except Exception:
            raise serializers.ValidationError(_('file not exist'))
        if not stroge.type.startswith('image'):
            raise serializers.ValidationError(_('file type is incorrect'))
        return value


class UserFollowSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()

    def validate_user(self, value):
        if not CustomUser.objects.filter(pk=value).exists():
            raise serializers.ValidationError(_('user not exist'))
        return value

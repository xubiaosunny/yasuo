from rest_framework import serializers
from django.utils.translation import gettext as _
from db.models import CustomUser


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('full_name', 'province', 'city')


class UserFollowSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()

    def validate_user(self, value):
        if not CustomUser.objects.filter(pk=value).exists():
            raise serializers.ValidationError(_('user not exist'))
        return value

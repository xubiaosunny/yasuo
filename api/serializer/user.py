from rest_framework import serializers
from django.utils.translation import gettext as _
from db.models import CustomUser


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('full_name', 'province', 'city')


class UserFollowSerializer(serializers.Serializer):
    user = serializers.IntegerField()

    def validate_user(self, value):
        try:
            user = CustomUser.objects.get(pk=value)
        except:
            raise serializers.ValidationError(_('user not exist'))
        return value

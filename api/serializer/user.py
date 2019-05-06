from rest_framework import serializers
from django.utils.translation import gettext as _
from db.models import CustomUser


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('full_name', 'province', 'city')

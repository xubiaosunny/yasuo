from rest_framework import serializers
from django.utils.translation import gettext as _
from db.models import CustomUser


class LoginSerializer(serializers.ModelSerializer):
    sms_code = serializers.CharField(help_text=_('SMS Code'))

    class Meta:
        model = CustomUser
        fields = ['phone', 'sms_code']
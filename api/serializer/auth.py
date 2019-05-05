from rest_framework import serializers
from django.utils.translation import gettext as _
from db.models import CustomUser, SMSCode
from utils.common.validators import is_chinese_phone_number


class PhoneSerializer(serializers.Serializer):
    phone = serializers.CharField(help_text=_('Phone Number'), validators=[is_chinese_phone_number])


class LoginSerializer(PhoneSerializer):
    sms_code = serializers.CharField(help_text=_('SMS Code'))

    def validate_sms_code(self, value):
        phone = self.initial_data['phone']
        if SMSCode.is_invalid(phone, value):
            raise serializers.ValidationError(_('The verification code is incorrect or has expired'))
        return value

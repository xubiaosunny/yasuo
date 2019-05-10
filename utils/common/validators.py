from rest_framework import serializers
from django.utils.translation import gettext as _
import re


def is_chinese_phone_number(value):
    reg = "1[3|4|5|6|7|8][0-9]{9}"
    if not re.findall(reg, value):
        raise serializers.ValidationError(_('The phone number is incorrect'))

from rest_framework import serializers
from django.utils.translation import gettext as _
from rest_framework.fields import empty

from db.models import OrderInfo


class OrderInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderInfo
        fields = ('payee', 'pay_method', 'amount', 'pay_item_class', 'pay_item_id')

class OrderCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderInfo
        fields = ('order_no', 'payee')




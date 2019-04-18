from rest_framework import serializers
from db.models import CustomUser

class LoginSerializer(serializers.ModelSerializer):
    # code = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = ['phone']
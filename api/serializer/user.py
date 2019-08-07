from rest_framework import serializers
from django.utils.translation import gettext as _
from db.models import CustomUser, LocalStorage, Certification, Message


class UserInfoSerializer(serializers.ModelSerializer):
    id_number = serializers.CharField(required=False, help_text=_('ID Number'))
    certified_file = serializers.IntegerField(required=False, help_text=_('Certified File'))

    class Meta:
        model = CustomUser
        fields = ('full_name', 'province', 'city', 'role', 'grade', 'work_place', 'avatar', 'introduction', 'id_number',
                  'certified_file')

    def validate_certified_file(self, value):
        if not value:
            return None
        if self.initial_data.get('role', None) != CustomUser.ROLE_CHOICES[0][0]:
            return None
        try:
            stroge = LocalStorage.objects.get(pk=value)
        except Exception:
            raise serializers.ValidationError(_('file not exist'))
        if not stroge.type.startswith('image'):
            raise serializers.ValidationError(_('file type is incorrect'))
        return stroge

    def update(self, instance, validated_data):
        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.province = validated_data.get('province', instance.province)
        instance.city = validated_data.get('city', instance.city)
        instance.role = validated_data.get('role', instance.role)
        instance.grade = validated_data.get('grade', instance.grade)
        instance.work_place = validated_data.get('work_place', instance.work_place)
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.introduction = validated_data.get('introduction', instance.introduction)
        instance.save()
        if instance.role == CustomUser.ROLE_CHOICES[0][0]:
            if not Certification.objects.filter(user=instance).exists():
                certification_data = {
                    'id_number': validated_data.get('id_number', ''),
                    'certified_file': validated_data.get('certified_file', None),
                    'status': Certification.STATUS_CHOICES[0][0]
                }
                Certification.objects.update_or_create(user=instance, defaults=certification_data)
        return instance


class UserFollowSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()

    def validate_user(self, value):
        if not CustomUser.objects.filter(pk=value).exists():
            raise serializers.ValidationError(_('user not exist'))
        return value

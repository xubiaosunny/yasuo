from rest_framework import serializers
from django.utils.translation import gettext as _
from django.core.exceptions import ObjectDoesNotExist
from db.models import Works, WorksComment, WorksQuestion, CustomUser, WorksQuestionReply


class WorksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Works
        fields = ('type', 'storage', 'title', 'summary', 'location')

    def validate_storage(self, value):
        if not value.type.startswith('image') and not value.type.startswith('video'):
            raise serializers.ValidationError(_('The file type is incorrect, Please upload an image or video'))
        return value


class WorksCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorksComment
        fields = ('voice', )

    def validate_voice(self, value):
        if not value.type.startswith('audio'):
            raise serializers.ValidationError(_('The file type is incorrect, Please upload an audio'))
        return value


class WorksQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorksQuestion
        fields = ('to', 'question')


class WorksAndQuestionSerializer(serializers.ModelSerializer):
    to = serializers.IntegerField(required=False)
    question = serializers.CharField(required=False)

    class Meta:
        model = Works
        fields = ('type', 'storage', 'title', 'summary', 'location', 'to', 'question')

    def validate_to(self, value):
        try:
            user = CustomUser.objects.get(pk=value)
        except ObjectDoesNotExist:
            raise serializers.ValidationError(_('User does not exist'))
        except Exception as e:
            raise e

        if user.role != CustomUser.ROLE_CHOICES[0][0]:
            raise serializers.ValidationError(_('Only ask the teacher questions'))
        return value


class WorksQuestionReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = WorksQuestionReply
        fields = ('voice', )

    def validate_voice(self, value):
        if not value.type.startswith('audio'):
            raise serializers.ValidationError(_('The file type is incorrect, Please upload an audio'))
        return value

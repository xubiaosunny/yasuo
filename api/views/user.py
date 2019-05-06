from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.forms.models import model_to_dict

from api.serializer.user import UserInfoSerializer
from utils.common.response import *


class UserInfoView(generics.GenericAPIView):
    """
    用户信息
    """
    serializer_class = UserInfoSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """
        获取用户信息
        """
        return response_200(model_to_dict(request.user, exclude=['password']))

    def patch(self, request):
        return response_200(model_to_dict(request.user, exclude=['password']))

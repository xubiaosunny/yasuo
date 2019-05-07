from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.forms.models import model_to_dict

from api.serializer.user import UserInfoSerializer, UserFollowSerializer
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


class UserFollowView(generics.GenericAPIView):
    """
    用户关注信息
    """
    serializer_class = UserFollowSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """
        获取关注和被关注的用户
        """
        data = {
            # 'follow_me': request.user.follow.all(),
            # 'my_follow': request.user.customuser_set.all()
        }
        return response_200(data)

    def post(self, request):
        """
        关注
        """
        serializer = UserFollowSerializer(data=request.data)
        if not serializer.is_valid():
            return response_400(serializer.errors)
        request.user.follow.add(serializer.data['user'])
        return response_200({})

    def delete(self, request):
        """
        取消关注
        """
        return response_200({})

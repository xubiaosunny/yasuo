from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from api.serializer.user import UserInfoSerializer, UserFollowSerializer
from utils.common.response import *
from db.db_models.auth import CustomUser


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
        return response_200(request.user.to_dict())

    def patch(self, request):
        serializer = UserInfoSerializer(data=request.data)
        if not serializer.is_valid():
            return response_400(serializer.errors)
        CustomUser.objects.filter(pk=request.user.id).update(**serializer.data)
        request.user.refresh_from_db()
        return response_200(request.user.to_dict())


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
            'my_follow': [u.to_dict() for u in request.user.follow.all()],
            'follow_me': [u.to_dict() for u in request.user.customuser_set.all()]
        }
        return response_200(data)

    def post(self, request):
        """
        关注
        """
        serializer = UserFollowSerializer(data=request.data)
        if not serializer.is_valid():
            return response_400(serializer.errors)
        request.user.follow.add(serializer.data['user_id'])
        return response_200(request.user.to_dict())

    def delete(self, request):
        """
        取消关注
        """
        serializer = UserFollowSerializer(data=request.data)
        if not serializer.is_valid():
            return response_400(serializer.errors)
        request.user.follow.remove(serializer.data['user_id'])
        return response_200({})

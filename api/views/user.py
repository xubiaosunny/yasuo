from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404

from api.serializer.user import UserInfoSerializer, UserFollowSerializer
from utils.common.response import *
from db.db_models.auth import CustomUser, Certification
from db.const import CITY


class UserCityView(generics.GenericAPIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        """
        获取城市列表, 如果传入`province` get参数则返回对应省份的城市列表，不传则返回所有省份对应的城市列表
        如：/api/user/cities/?province=广东省
        """
        province = request.GET.get('province', None)
        if province is None:
            data = [{"name": k, "city": v} for k, v in CITY.items()]
            data.sort(key=lambda x: x['name'])
        else:
            data = CITY.get(province, [])

        return response_200({'cities': data})


class UserGradeView(generics.GenericAPIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        """
        获取年级选项
        """
        data = [{'label': g[1], 'value': g[0]} for g in CustomUser.GRADE_CHOICES]
        return response_200({'grades': data})


class UserInfoView(generics.GenericAPIView):
    """
    用户信息
    """
    serializer_class = UserInfoSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """
        获取用户信息, 默认为本人的用户信息，传入get参数id则获取对应id的用户信息
        如：/api/user/info/?id=1
        """
        user_id = request.GET.get('id', None)
        if user_id:
            user = get_object_or_404(CustomUser, pk=user_id)
        else:
            user = request.user

        return response_200(user.to_dict())

    def patch(self, request):
        """更新用户信息"""
        serializer = UserInfoSerializer(instance=request.user, data=request.data)
        if not serializer.is_valid():
            return response_400(serializer.errors)
        user = serializer.save()
        return response_200(user.to_dict())


class UserFollowView(generics.GenericAPIView):
    """
    用户关注信息
    """
    serializer_class = UserFollowSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """
        获取关注和被关注的用户，默认返回为本人的用户关注信息，传入get参数id则获取对应id的用户关注信息
        如：/api/user/follow/?id=1
        """
        user_id = request.GET.get('id', None)
        if user_id:
            user = get_object_or_404(CustomUser, pk=user_id)
        else:
            user = request.user

        data = {
            'my_follow': [u.to_dict() for u in user.follow.all()],
            'follow_me': [u.to_dict() for u in user.customuser_set.all()]
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
        return response_200(request.data)

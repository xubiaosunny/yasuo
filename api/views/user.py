from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404

from api.serializer.user import UserInfoSerializer, UserFollowSerializer
from utils.common.response import *
from db.models import CustomUser, Works, Message
from db.const import CITY
from utils.tasks.push import *
from rest_framework import serializers


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


class UserWorkspaceOfTeacherView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """
        获取老师们的工作地址
        """
        users = CustomUser.objects.filter(role=CustomUser.ROLE_CHOICES[0][0]).values('work_place').distinct()
        return response_200({'work_places': [u['work_place'] for u in users]})


class UserAllWorkspaceOfTeacherView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """
        获取老师们的工作地址
        """
        users = CustomUser.objects.filter(role=CustomUser.ROLE_CHOICES[0][0]).values('work_place').distinct()
        return response_200({'work_places': [u['work_place'] for u in users]})


class UserTeacherOfWorkspaceView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """
        GET参数`work_space`，获取该学校（单位）老师们
        """
        work_space = request.GET.get('work_space', None)
        if work_space:
            users = CustomUser.objects.filter(work_place=work_space)
            return response_200({'teachers': [u.to_dict() for u in users]})
        else:
            return response_404()


class UserInfoView(generics.GenericAPIView):
    """
    用户信息
    """
    serializer_class = UserInfoSerializer
    permission_classes = (AllowAny,)

    def get(self, request):
        """
        获取用户信息, 默认为本人的用户信息，传入get参数id则获取对应id的用户信息
        如：/api/user/info/?id=1
        """
        user_id = request.GET.get('id', None)
        if user_id:
            user = get_object_or_404(CustomUser, pk=user_id)
        else:
            if request.user.is_anonymous:
                return response_403()
            user = request.user
        return response_200(user.to_dict(guest=request.user))

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
        send_push_j(serializer.data['user_id'], '%s关注了你' % (request.user.full_name or request.user.phone, ),
                    class_name=Message.CLASS_NAME_CHOICES[2][0], class_id=serializer.data['user_id'])
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


class UserWorksView(generics.GenericAPIView):
    """
    用户作品
    可选GET参数`storage_type`：
        * image: 图片
        * video: 视频
    """
    serializer_class = serializers.Serializer
    permission_classes = (AllowAny,)

    def get(self, request, _id):
        storage_type = request.GET.get('storage_type', None)
        works_s = Works.objects.filter(is_delete=False, user_id=_id)
        if storage_type:
            works_s = works_s.filter(storage__type__startswith=storage_type)

        return response_200({'works': [w.details() for w in works_s]})


class UserFollowTeacherView(generics.GenericAPIView):
    """
    用户关注的老师
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        teachers = request.user.follow.filter(role=CustomUser.ROLE_CHOICES[0][0])
        recommends = CustomUser.objects.filter(role=CustomUser.ROLE_CHOICES[0][0]).exclude(
            pk__in=teachers).exclude(pk=request.user.id).order_by('?')[:5]
        return response_200({'users': [u.to_dict() for u in teachers], 'recommends': [u.to_dict() for u in recommends]})


class UserFollowStudentView(generics.GenericAPIView):
    """
    用户关注的学生
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        students = request.user.follow.filter(role=CustomUser.ROLE_CHOICES[1][0])
        recommends = CustomUser.objects.filter(role=CustomUser.ROLE_CHOICES[1][0]).exclude(
            pk__in=students).exclude(pk=request.user.id).order_by('?')[:5]
        return response_200({'users': [u.to_dict() for u in students], 'recommends': [u.to_dict() for u in recommends]})


class UserFollowWorksView(generics.GenericAPIView):
    """
    用户关注的人的最新动态
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        follows = request.user.follow.all()
        works_s = Works.objects.filter(user__in=follows, is_delete=False).order_by('-create_time')
        return response_200({'works': [works.details(user=request.user) for works in works_s]})


class UserMessageView(generics.GenericAPIView):
    """
    用户消息
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        messages = Message.objects.filter(user=request.user).order_by('-push_time')
        return response_200({'messages': [message.details() for message in messages]})


class UserMessageReadView(generics.GenericAPIView):
    """
    标记消息已读
    """
    serializer_class = serializers.Serializer
    permission_classes = (IsAuthenticated,)

    def put(self, request, _id):
        Message.objects.filter(pk=_id).update(is_read=True)
        return response_200({})

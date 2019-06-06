from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.utils.translation import gettext as _
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist

from utils.common.response import *
from utils.common.permissions import IsTeacher, IsStudent, my_permission_classes
from api.serializer.works import WorksSerializer, WorksCommentSerializer, WorksQuestionSerializer
from db.models import Works, WorksComment, WorksQuestion


class WorksView(generics.GenericAPIView):
    """
    作品
    """
    serializer_class = WorksSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """获取自己的所有作品，传入get参数id获取对应的作品信息"""
        works_id = request.GET.get('id', None)
        if works_id:
            works = get_object_or_404(Works, pk=works_id)
            return response_200(works.details(user=request.user))
        else:
            works_s = request.user.works_set.filter(is_delete=False)
            return response_200({'works': [works.details(user=request.user) for works in works_s]})

    def post(self, request):
        """创建作品"""
        serializer = WorksSerializer(data=request.data)
        if not serializer.is_valid():
            return response_400(serializer.errors)
        works = Works.objects.create(user=request.user, **serializer.validated_data)
        return response_200(works.details())

    def delete(self, request):
        """删除作品，传入get参数id删除对应作品"""
        works_id = request.GET.get('id', None)
        if not works_id:
            return response_404()
        works = get_object_or_404(Works, pk=works_id, user=request.user, is_delete=False)
        works.mark_deleted()
        return response_200(works.details())


class WorksFavoriteView(generics.GenericAPIView):
    serializer_class = serializers.Serializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, _id):
        """点赞"""
        works = get_object_or_404(Works, pk=_id)
        works.favorite.add(request.user)
        return response_200(works.details(user=request.user))

    def delete(self, request, _id):
        """取消点赞"""
        works = get_object_or_404(Works, pk=_id)
        works.favorite.remove(request.user)
        return response_200(works.details(user=request.user))


class WorksCommentView(generics.GenericAPIView):
    serializer_class = WorksCommentSerializer
    permission_classes = (IsAuthenticated, )

    def get(self, request, _id):
        """获取_id对应作品的所有评论"""
        comments = WorksComment.objects.filter(works_id=_id)
        return response_200({'comments': [comment.details() for comment in comments]})

    @my_permission_classes((IsTeacher, ))
    def post(self, request, _id):
        """评论"""
        works = get_object_or_404(Works, pk=_id)
        serializer = WorksCommentSerializer(data=request.data)
        if not serializer.is_valid():
            return response_400(serializer.errors)
        try:
            WorksComment.objects.get(user=request.user, works=works)
        except ObjectDoesNotExist:
            comment = WorksComment.objects.create(user=request.user, works=works, **serializer.validated_data)
            return response_200(comment.details())
        except Exception as e:
            raise e
        else:
            return response_400({'voice': _('You have commented on the work')})


class WorksQuestionView(generics.GenericAPIView):
    serializer_class = WorksQuestionSerializer
    permission_classes = (IsAuthenticated, )

    def get(self, request, _id):
        """获取_id对应作品的所有提问"""
        questions = WorksQuestion.objects.filter(works_id=_id)
        return response_200({'questions': [question.details() for question in questions]})

    @my_permission_classes((IsStudent,))
    def post(self, request, _id):
        """就_id对应的作品进行提问"""
        works = get_object_or_404(Works, pk=_id)
        serializer = WorksQuestionSerializer(data=request.data)
        if not serializer.is_valid():
            return response_400(serializer.errors)
        question = WorksQuestion.objects.create(works=works, **serializer.validated_data)
        return response_200(question.details())

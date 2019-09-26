from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.utils.translation import gettext as _
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist

from utils.common.response import *
from utils.common.permissions import IsTeacher, IsStudent, my_permission_classes
from api.serializer.works import WorksSerializer, WorksCommentSerializer, WorksQuestionSerializer, \
    WorksAndQuestionSerializer, WorksQuestionReplySerializer
from db.models import Works, WorksComment, WorksQuestion, WorksQuestionReply, Message
from utils.tasks.push import *


class WorksCategoryView(generics.GenericAPIView):
    permission_classes = (AllowAny, )

    def get(self, request):
        """获取作品可选分类"""
        return response_200({'category': [{'label': c[1], 'value': c[0]} for c in Works.TYPE_CHOICES]})


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
        # send_push_j(works.user_id, '%s点赞了你的作品' % (request.user.full_name or request.user.phone,),
        #             class_name=Message.CLASS_NAME_CHOICES[0][0], class_id=works.id)
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
        last_question = WorksQuestion.objects.filter(works_id=_id, to=request.user).order_by('-create_time').first()
        return response_200({
            'is_commented': WorksComment.objects.filter(works_id=_id, user=request.user).exists(),
            'to_me_last_question_id': last_question.id if last_question else None,
            'comments': [comment.details() for comment in comments]
        })

    @my_permission_classes((IsTeacher, ))
    def post(self, request, _id):
        """评论"""
        works = get_object_or_404(Works, pk=_id)
        serializer = WorksCommentSerializer(data=request.data)
        if not serializer.is_valid():
            return response_400(serializer.errors)
        comment = WorksComment.objects.create(user=request.user, works=works, **serializer.validated_data)
        send_push_j(works.user_id, '%s评论了你的作品' % (request.user.full_name or request.user.phone,),
                    class_name=Message.CLASS_NAME_CHOICES[3][0], class_id=comment.id)
        return response_200(comment.details())


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
        last_question = WorksQuestion.objects.filter(
            works=works, to=serializer.validated_data["to"]).order_by("-create_time").first()
        if last_question and last_question.worksquestionreply_set.count() == 0:
            return response_400({"to": "老师还未回复你上一个提问，请稍后再向他提问"})
        question = WorksQuestion.objects.create(works=works, **serializer.validated_data)
        send_push_j(question.to_id, '%s向你提问了' % (request.user.full_name or request.user.phone,),
                    class_name=Message.CLASS_NAME_CHOICES[1][0], class_id=question.id)
        return response_200(question.details())


class WorksDirectQuestionView(generics.GenericAPIView):
    serializer_class = WorksAndQuestionSerializer
    permission_classes = (IsAuthenticated, )

    @my_permission_classes((IsStudent,))
    def post(self, request):
        """
        发布作品并进行提问
        """
        serializer = WorksAndQuestionSerializer(data=request.data)
        if not serializer.is_valid():
            return response_400(serializer.errors)
        works = Works.objects.create(
            user=request.user, type=serializer.validated_data.get('type', None),
            title=serializer.validated_data.get('title', ''),
            storage=serializer.validated_data['storage'], summary=serializer.validated_data.get('summary', ''),
            location=serializer.validated_data.get('location', ''),
            is_private=serializer.validated_data.get('is_private', False),)
        to = serializer.validated_data.get('to', None)
        if to:
            WorksQuestion.objects.create(works=works, to_id=to, question=serializer.validated_data.get('question', ''))
        return response_200(works.details())


class WorksQuestionReplyView(generics.GenericAPIView):
    serializer_class = WorksQuestionReplySerializer
    permission_classes = (IsAuthenticated, )

    def get(self, request, _id):
        """获取_id的提问的所有回复"""
        reply_s = WorksQuestionReply.objects.filter(works_question_id=_id)
        return response_200({'reply': [reply.details() for reply in reply_s]})

    @my_permission_classes((IsTeacher,))
    def post(self, request, _id):
        """
        对提问进行回复
        """
        question = get_object_or_404(WorksQuestion, pk=_id)
        if question.to != request.user:
            return response_403(_("Can't reply to the question"))
        serializer = WorksQuestionReplySerializer(data=request.data)
        if not serializer.is_valid():
            return response_400(serializer.errors)
        question_reply = WorksQuestionReply.objects.create(works_question=question, **serializer.validated_data)
        send_push_j(question.works.user_id, '%s回复了你的提问' % (request.user.full_name or request.user.phone,),
                    class_name=Message.CLASS_NAME_CHOICES[1][0], class_id=question.id)
        return response_200(question_reply.details())

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404

from utils.common.response import *
from api.serializer.storage import LocalStorageSerializer
from db.models import LocalStorage


class LocalStorageView(generics.GenericAPIView):
    serializer_class = LocalStorageSerializer
    permission_classes = (AllowAny,)

    def get(self, request):
        """传入get参数`id`获取该实例的详细信息"""
        instance = get_object_or_404(LocalStorage, pk=request.GET.get('id'))
        return response_200(instance.details())

    def post(self, request):
        """本地存储，上传文件"""
        serializer = LocalStorageSerializer(data=request.data, user=request.user)
        if not serializer.is_valid():
            return response_400(serializer.errors)
        instance = serializer.save()
        return response_200(instance.details())

from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.utils.translation import gettext as _
from db.models import AppUpdateLog
from utils.common.response import *


class AppUpdateLogView(generics.GenericAPIView):
    permission_classes = (AllowAny, )

    def get(self, request):
        """
        获取所有更新列表

        > 参数`source`: ios, android
        """
        filters = {}
        source = request.GET.get('source', None)
        if source:
            filters['source'] = source
        logs = AppUpdateLog.objects.filter(**filters).order_by('-pk')
        return response_200({'update_logs': [i.details() for i in logs]})


class AppUpdateLogLastView(generics.GenericAPIView):
    permission_classes = (AllowAny, )

    def get(self, request):
        """
        获取最新一条更新

        > 参数`source`: ios, android
        """
        filters = {}
        source = request.GET.get('source', None)
        if source:
            filters['source'] = source
        log = AppUpdateLog.objects.filter(**filters).order_by('-pk').first()
        data = log.details() if log else {}
        return response_200(data)

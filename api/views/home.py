from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.utils.translation import gettext as _
from rest_framework import serializers
from db.models import Works
from utils.common.response import *


class IndexView(generics.ListAPIView):
    permission_classes = (AllowAny, )

    def get(self, request):
        """传入get参数`city`则返回对应发布在城市的作品，否则返回所有作品（按照评论数排序）"""
        city = request.GET.get('city', None)
        if city:
            works_s = Works.objects.filter(is_delete=False, location=city)
        else:
            works_s = Works.objects.filter(is_delete=False)
        data = [works.details(user=request.user) if request.user.is_anonymous else works.details() for works in works_s]
        data = sorted(data, key=lambda x: x['comment_number'], reverse=True)
        return response_200({'works': data})

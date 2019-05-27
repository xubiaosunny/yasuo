from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.utils.translation import gettext as _
from django.shortcuts import get_object_or_404

from utils.common.response import *
from api.serializer.works import WorksSerializer
from db.models import Works


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
            return response_200(works.details())
        else:
            works_s = request.user.works_set.filter(is_delete=False)
            print([works.details() for works in works_s])
            return response_200({'works': [works.details() for works in works_s]})

    def post(self, request):
        """创建作品"""
        serializer = WorksSerializer(data=request.data)
        if not serializer.is_valid():
            return response_400(serializer.errors)
        works = Works.objects.create(user=request.user, **serializer.validated_data)
        return response_200(works.details())

    def delete(self, request):
        """删除作品"""
        pass

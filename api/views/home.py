from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.utils.translation import gettext as _
from rest_framework import serializers
from db.models import Works
from utils.common.response import *

INDEX_SQL = """SELECT w.*, c.comment_conut
    FROM (
        SELECT
            works_id, count(works_id) AS comment_conut
        FROM db_workscomment
        GROUP BY works_id
    ) c
RIGHT JOIN db_works w
on w.id=c.works_id
where w.is_delete is false AND w.is_private IS FALSE 
order by c.comment_conut DESC
LIMIT %s, %s;
"""


class IndexView(generics.ListAPIView):
    permission_classes = (AllowAny, )

    def get(self, request):
        """
        GET参数:

        * `city`则返回对应发布在城市的作品，否则返回所有作品（按照评论数排序）

        * `start`指定开始位置（按照评论数排序的），默认0

        * `limit`来限制返回个数，默认10

        eg.

        > `/api/home/?start=10&limit=10`
        """
        city = request.GET.get('city', None)
        start = int(request.GET.get('start', 0))
        limit = int(request.GET.get('limit', 10))
        if city:
            works_s = Works.objects.filter(is_delete=False, location=city).order_by('-id')[start:start + limit]
        else:
            works_s = Works.objects.raw(INDEX_SQL, params=[start, start + limit])
        data = [works.details(user=request.user) if request.user.is_anonymous else works.details() for works in works_s]
        return response_200({'works': data})

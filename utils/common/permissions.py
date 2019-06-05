from rest_framework.permissions import BasePermission
import hashlib
import datetime

from db.models import CustomUser
from yasuo.config import ACCESS_KEY


class SignaturePermission(BasePermission):
    def has_permission(self, request, view):
        # "Signature xxxxxxxxxxx %Y-%m-%dT%H:%M:%S"
        authentication = str(request.META.get('HTTP_AUTHORIZATION', None))
        try:
            authentication_type, signature, date_str = authentication.split(" ", maxsplit=2)
            datetime.datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S')
        except Exception:
            return False
        if authentication_type != "Signature":
            return False
        m = hashlib.md5()
        m.update(ACCESS_KEY.encode('utf-8'))
        m.update(request.path.encode('utf-8'))
        m.update(date_str.encode('utf-8'))
        return signature == m.hexdigest()


class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == CustomUser.ROLE_CHOICES[0][0]


class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == CustomUser.ROLE_CHOICES[1][0]

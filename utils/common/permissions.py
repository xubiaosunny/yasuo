from rest_framework.permissions import BasePermission
import hashlib
import datetime
import functools

from db.models import CustomUser
from yasuo.config import ACCESS_KEY


def my_permission_classes(permission_classes):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, request, *args, **kwargs):
            for permission_class in permission_classes:
                permission = permission_class()
                if not permission.has_permission(request, self):
                    self.permission_denied(
                        request, message=getattr(permission, 'message', None)
                    )
            return func(self, request, *args, **kwargs)
        return wrapper
    return decorator


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

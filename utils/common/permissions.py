from rest_framework.permissions import BasePermission
import hashlib

from yasuo.config import ACCESS_KEY


class SignaturePermission(BasePermission):
    def has_permission(self, request, view):
        signature = str(request.META.get('HTTP_AUTHORIZATION', None))
        date = request.META.get('HTTP_DATE', None)  # '%a, %d %b %Y %H:%M:%S GMT'
        if signature is None or date is None:
            return False
        m = hashlib.md5(ACCESS_KEY.encode('utf-8'))
        m.update(request.path.encode('utf-8'))
        m.update(date.encode('utf-8'))
        return signature == m.hexdigest()

from rest_framework.permissions import BasePermission


class TestDemo(BasePermission):
    def has_permission(self, request, view):
        return True

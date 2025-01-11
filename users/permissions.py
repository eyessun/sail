from rest_framework import permissions


class IsAdminUserCustom(permissions.BasePermission):
    """
    只有管理员用户可以访问
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'
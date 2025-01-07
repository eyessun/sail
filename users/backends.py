# users/backends.py

from django.contrib.auth.backends import BaseBackend
from .models import AdminUser, StaffUser

class PhoneBackend(BaseBackend):
    """
    自定义认证后端，使用手机号和角色进行认证
    """

    def authenticate(self, request, phone=None, password=None, role=None, **kwargs):
        if phone is None or role is None:
            return None

        user = None
        if role == 'admin':
            try:
                user = AdminUser.objects.get(phone=phone)
            except AdminUser.DoesNotExist:
                return None
        elif role == 'normal':
            try:
                user = StaffUser.objects.get(phone=phone)
            except StaffUser.DoesNotExist:
                return None
        else:
            return None

        if user.check_password(password) and user.is_active:
            return user

        return None

    def get_user(self, user_id):
        try:
            return AdminUser.objects.get(pk=user_id)
        except AdminUser.DoesNotExist:
            try:
                return StaffUser.objects.get(pk=user_id)
            except StaffUser.DoesNotExist:
                return None

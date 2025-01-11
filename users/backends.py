from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist


class PhoneBackend(BaseBackend):
    """
    使用手机号进行身份验证的后端
    """

    def authenticate(self, request, phone=None, password=None, **kwargs):
        """
        基于手机号和密码验证用户身份
        """
        try:
            # 尝试通过手机号查找用户
            user = get_user_model().objects.get(phone=phone)
        except ObjectDoesNotExist:
            return None

        # 检查密码是否正确
        if user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        """
        获取用户对象，Django 默认会调用这个方法来获取用户实例
        """
        try:
            return get_user_model().objects.get(pk=user_id)
        except ObjectDoesNotExist:
            return None
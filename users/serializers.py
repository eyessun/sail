# users/serializers.py
import time
import time
import logging
logger = logging.getLogger(__name__)
from rest_framework import serializers
from .models import AdminUser, StaffUser, LoginAttempt
from django.contrib.auth import authenticate
from django.utils import timezone
from datetime import timedelta, datetime


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=20, required=True, help_text='用户手机号')
    password = serializers.CharField(write_only=True, required=True, help_text='用户密码')
    role = serializers.ChoiceField(choices=LoginAttempt.ROLE_CHOICES, required=True, help_text='用户角色')

    def validate(self, data):
        phone = data.get('phone')
        password = data.get('password')
        role = data.get('role')

        # 尝试获取用户
        user = None
        if role == 'admin':
            try:
                user = AdminUser.objects.get(phone=phone)
            except AdminUser.DoesNotExist:
                raise serializers.ValidationError('手机尚未注册。')
        elif role == 'normal':
            try:
                user = StaffUser.objects.get(phone=phone)
            except StaffUser.DoesNotExist:
                logger.warning(f"StaffUser with phone {phone} does not exist or invalid role.")
                raise serializers.ValidationError('手机号或角色无效。')
        else:
            logger.warning(f"Invalid role provided: {role}")
            raise serializers.ValidationError('无效的角色。')

        # 检查用户是否激活
        if not user.is_active:
            logger.warning(f"User account {phone} is inactive.")
            raise serializers.ValidationError('用户账户已被禁用。')

        # 获取或创建LoginAttempt记录
        login_attempt, created = LoginAttempt.objects.get_or_create(phone=phone, role=role)
        if created:
            print(f"Created new LoginAttempt for {phone} with role {role}")
        else:
            print(f"Using existing LoginAttempt for {phone} with role {role}")

        # 检查是否处于锁定状态
        if login_attempt.lockout_until and login_attempt.lockout_until > timezone.now():
            remaining_seconds = (login_attempt.lockout_until - timezone.now()).total_seconds()
            remaining_minutes = int(remaining_seconds // 60) + 1  # 向上取整
            raise serializers.ValidationError(f"输入的密码次数过多，禁用{remaining_minutes}分钟。")

        # 进行认证
        user_auth = authenticate(phone=phone, password=password, role=role)
        if user_auth is None:
            logger.warning(f"Authentication failed for phone: {phone}, role: {role}")
            # 认证失败，增加失败次数
            login_attempt.failed_attempts += 1
            if login_attempt.failed_attempts >= 5:
                # 达到最大失败次数，设置锁定时间

                timenow = timezone.now()

                # 转换为本地时区时间（Asia/Shanghai）
                local_now = timezone.localtime(timenow)

                login_attempt.lockout_until = local_now + timedelta(minutes=5)
                login_attempt.failed_attempts = 0  # 重置失败次数
                print(f"用户 {phone} 锁定时间: {login_attempt.lockout_until}")
            login_attempt.save()
            if login_attempt.lockout_until:
                raise serializers.ValidationError("输入的密码次数过多，禁用5分钟。")
            else:
                raise serializers.ValidationError('手机号或密码错误。')

        # 认证成功，重置失败次数和锁定时间
        login_attempt.failed_attempts = 0
        login_attempt.lockout_until = None
        login_attempt.save()


        # 将用户添加到验证数据中
        data['user'] = user
        return data

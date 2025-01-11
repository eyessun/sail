from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate

from utils.response import error_response
from django.utils import timezone
from rest_framework import serializers
from .models import Role
from .serializer import PermissionSerializer
from .serializer.RoleSerializer import RoleSerializer

from rest_framework import serializers
from .models import Permission

from django.contrib.auth.password_validation import validate_password


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=20, required=True, help_text='用户手机号')
    password = serializers.CharField(write_only=True, required=True, help_text='用户密码')

    def validate(self, data):
        phone = data.get('phone')
        password = data.get('password')

        # 尝试获取用户
        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            raise serializers.ValidationError(error_response(1001, "手机号或密码错误"))

        # 验证密码
        if not user.check_password(password):
            raise serializers.ValidationError(error_response(1001, "手机号或密码错误"))

        # 检查用户是否激活
        if not user.is_active:
            raise serializers.ValidationError(error_response(1001, "用户账户已被禁用。"))
        data['user'] = user
        return data

            # 获取或创建LoginAttempt记录
            # login_attempt, created = LoginAttempt.objects.get_or_create(phone=phone, role=role)
            # # if created:
            # #     print(f"Created new LoginAttempt for {phone} with role {role}")
            # # else:
            # #     print(f"Using existing LoginAttempt for {phone} with role {role}")
            #
            # # 检查是否处于锁定状态
            # if login_attempt.lockout_until and login_attempt.lockout_until > timezone.now():
            #     remaining_seconds = (login_attempt.lockout_until - timezone.now()).total_seconds()
            #     remaining_minutes = int(remaining_seconds // 60) + 1  # 向上取整
            #     raise serializers.ValidationError(error_response(1002, f"输入的密码次数过多，禁用{remaining_minutes}分钟。"))
            #
            # # 进行认证
            # user_auth = authenticate(phone=phone, password=password)
            # if user_auth is None:
            #     # 认证失败，增加失败次数
            #     login_attempt.failed_attempts += 1
            #     if login_attempt.failed_attempts >= 5:
            #         # 达到最大失败次数，设置锁定时间
            #         timenow = timezone.now()
            #         # 转换为本地时区时间（Asia/Shanghai）
            #         local_now = timezone.localtime(timenow)
            #         login_attempt.lockout_until = local_now + timedelta(minutes=5)
            #         login_attempt.failed_attempts = 0  # 重置失败次数
            #     login_attempt.save()
            #     if login_attempt.lockout_until:
            #         raise serializers.ValidationError(error_response(1002, "输入的密码次数过多，禁用5分钟。"))
            #     else:
            #         raise serializers.ValidationError(error_response(1001, "手机号或密码错误。"))
            #
            # # 认证成功，重置失败次数和锁定时间
            # login_attempt.failed_attempts = 0
            # login_attempt.lockout_until = None
            # login_attempt.save()

            # 将用户添加到验证数据中

class UserSerializer(serializers.ModelSerializer):
    """
    用户序列化器：用于创建和更新用户，处理密码加密，并验证角色。
    """
    password = serializers.CharField(write_only=True, required=True, help_text='用户密码')
    role = RoleSerializer(read_only=False)  # 角色字段关联到 RoleSerializer

    class Meta:
        model = User
        fields = ['id', 'name', 'phone', 'password', 'role', 'is_active', 'date_joined', 'is_staff']
        read_only_fields = ['id', 'date_joined']  # id 和 date_joined 只读

    def validate_password(self, value):
        """
        验证密码是否合法
        """
        validate_password(value)  # 使用 Django 提供的密码验证机制
        return value

    def create(self, validated_data):
        """
        创建用户时，自动对密码进行加密
        """
        password = validated_data.pop('password')  # 提取密码字段
        role_data = validated_data.pop('role')  # 提取角色字段

        # 创建角色对象
        role_instance = Role.objects.get(name=role_data['name'])  # 根据角色名称获取角色实例

        user = User.objects.create(role=role_instance, **validated_data)  # 创建用户实例并关联角色
        user.set_password(password)  # 对密码进行加密
        user.save()  # 保存用户
        return user

    def update(self, instance, validated_data):
        """
        更新用户信息时，处理密码加密
        """
        password = validated_data.get('password', None)  # 获取新的密码（如果有）
        if password:
            instance.set_password(password)  # 对新密码加密

        # 获取角色信息并更新
        role_data = validated_data.get('role', None)
        if role_data:
            role_instance = Role.objects.get(name=role_data['name'])  # 根据角色名称获取角色实例
            instance.role = role_instance  # 更新角色

        # 更新其他字段
        for attr, value in validated_data.items():
            if attr not in ['password', 'role']:  # 忽略密码和角色字段
                setattr(instance, attr, value)

        instance.save()  # 保存用户更新
        return instance

class UserSerializer(serializers.ModelSerializer):
    """
    用户序列化器：用于创建和更新用户，处理密码加密，并验证角色。
    """
    password = serializers.CharField(write_only=True, required=True, help_text='用户密码')
    role = RoleSerializer(read_only=False)  # 角色字段关联到 RoleSerializer

    class Meta:
        model = User
        fields = ['id', 'name', 'phone', 'password', 'role', 'is_active', 'date_joined', 'is_staff']
        read_only_fields = ['id', 'date_joined']  # id 和 date_joined 只读

    def validate_password(self, value):
        """
        验证密码是否合法
        """
        validate_password(value)  # 使用 Django 提供的密码验证机制
        return value

    def create(self, validated_data):
        """
        创建用户时，自动对密码进行加密
        """
        password = validated_data.pop('password')  # 提取密码字段
        role_data = validated_data.pop('role')  # 提取角色字段

        # 创建角色对象
        role_instance = Role.objects.get(name=role_data['name'])  # 根据角色名称获取角色实例

        user = User.objects.create(role=role_instance, **validated_data)  # 创建用户实例并关联角色
        user.set_password(password)  # 对密码进行加密
        user.save()  # 保存用户
        return user

    def update(self, instance, validated_data):
        """
        更新用户信息时，处理密码加密
        """
        password = validated_data.get('password', None)  # 获取新的密码（如果有）
        if password:
            instance.set_password(password)  # 对新密码加密

        # 获取角色信息并更新
        role_data = validated_data.get('role', None)
        if role_data:
            role_instance = Role.objects.get(name=role_data['name'])  # 根据角色名称获取角色实例
            instance.role = role_instance  # 更新角色

        # 更新其他字段
        for attr, value in validated_data.items():
            if attr not in ['password', 'role']:  # 忽略密码和角色字段
                setattr(instance, attr, value)

        instance.save()  # 保存用户更新
        return instance





class PermissionSerializer(serializers.ModelSerializer):
    """
    权限序列化器：用于展示每个权限的详细信息。
    """
    class Meta:
        model = Permission
        fields = ['id', 'name', 'description']
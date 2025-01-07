# users/models.py

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from django.contrib.auth.models import Group, Permission

class AbstractUserBase(models.Model):
    """
    抽象基类，包含所有用户共有的字段
    """
    name = models.CharField(max_length=255, verbose_name='姓名')
    phone = models.CharField(max_length=20, verbose_name='手机号')
    password = models.CharField(max_length=128, verbose_name='密码')  # AbstractBaseUser 已包含密码字段
    is_active = models.BooleanField(default=True, verbose_name='是否激活')
    date_joined = models.DateTimeField(default=timezone.now, verbose_name='加入时间')

    class Meta:
        abstract = True

class AdminUserManager(BaseUserManager):
    """
    管理员用户管理器
    """
    def create_user(self, phone, name, password=None, **extra_fields):
        if not phone:
            raise ValueError('管理员必须有一个手机号')
        user = self.model(phone=phone, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, name, password=None, **extra_fields):
        user = self.create_user(phone, name, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class AdminUser(AbstractBaseUser, PermissionsMixin, AbstractUserBase):
    """
    管理员用户模型
    """
    is_staff = models.BooleanField(default=True, verbose_name='是否为员工')  # 必须字段
    # 显式设置 related_name 来避免冲突
    groups = models.ManyToManyField(Group, related_name='admin_users', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='admin_user_permissions', blank=True)
    objects = AdminUserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['name']

    class Meta:
        verbose_name = '管理员用户'
        verbose_name_plural = '管理员用户'
        unique_together = ('phone',)  # 确保手机号在管理员中唯一

    def __str__(self):
        return f"{self.name} ({self.phone}) - 管理员"

class StaffUserManager(BaseUserManager):
    """
    普通用户管理器
    """
    def create_user(self, phone, name, password=None, **extra_fields):
        if not phone:
            raise ValueError('普通用户必须有一个手机号')
        user = self.model(phone=phone, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class StaffUser(AbstractBaseUser, PermissionsMixin, AbstractUserBase):
    """
    普通用户（业务员）模型
    """
    # 显式设置 related_name 来避免冲突
    groups = models.ManyToManyField(Group, related_name='staff_users', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='staff_user_permissions', blank=True)
    objects = StaffUserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['name']

    class Meta:
        verbose_name = '普通用户'
        verbose_name_plural = '普通用户'
        unique_together = ('phone',)  # 确保手机号在普通用户中唯一

    def __str__(self):
        return f"{self.name} ({self.phone}) - 普通用户"

class LoginAttempt(models.Model):
    """
    模型用于跟踪用户的登录失败次数和锁定时间
    """
    ROLE_CHOICES = (
        ('admin', '管理员'),
        ('normal', '普通用户'),
    )
    phone = models.CharField(max_length=20, verbose_name='手机号')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, verbose_name='角色')
    failed_attempts = models.IntegerField(default=0, verbose_name='失败尝试次数')
    lockout_until = models.DateTimeField(null=True, blank=True, verbose_name='锁定截止时间')

    class Meta:
        unique_together = ('phone', 'role')  # 同一手机号在不同角色中唯一

    def __str__(self):
        return f"{self.phone} - {self.role} - 尝试次数: {self.failed_attempts}"

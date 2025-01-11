from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone

class Role(models.Model):
    """
    角色模型，角色控制访问权限
    """
    name = models.CharField(max_length=50, unique=True, verbose_name='角色名称')
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name='角色描述')

    class Meta:
        verbose_name = '角色'
        verbose_name_plural = '角色'

    def __str__(self):
        return self.name

class Permission(models.Model):
    """
    权限模型，表示一项具体权限（如操作权限或菜单权限）
    """
    name = models.CharField(max_length=255, unique=True, verbose_name='权限名称')
    codename = models.CharField(max_length=100, unique=True, verbose_name='权限代号')
    description = models.TextField(blank=True, null=True, verbose_name='权限描述')

    class Meta:
        verbose_name = '权限'
        verbose_name_plural = '权限'

    def __str__(self):
        return self.name

if serializer.is_valid():
    user = serializer.create()
    print(f'用户 {user.name} 创建成功！')
else:
    print(serializer.errors)

class RolePermission(models.Model):
    """
    角色和权限关联模型，表示某个角色拥有的权限
    """
    role = models.ForeignKey(Role, on_delete=models.CASCADE, verbose_name='角色')
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, verbose_name='权限')

    class Meta:
        unique_together = ('role', 'permission')

    def __str__(self):
        return f"{self.role.name} - {self.permission.name}"

class Menu(models.Model):
    """
    菜单模型，表示系统中的每个菜单项
    """
    title = models.CharField(max_length=100, verbose_name="菜单标题")
    route = models.CharField(max_length=200, verbose_name="路由路径")
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    order = models.IntegerField(default=0, verbose_name="菜单排序")

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

class RoleMenu(models.Model):
    """
    角色菜单关联模型，表示某个角色可以访问哪些菜单
    """
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('role', 'menu')

    def __str__(self):
        return f"{self.role.name} - {self.menu.title}"

class UserManager(BaseUserManager):
    """
    自定义用户管理器
    """
    def create_user(self, phone, name, password=None, **extra_fields):
        """
        创建普通用户
        """
        if not phone:
            raise ValueError('用户必须有手机号')
        user = self.model(phone=phone, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, name, password=None, **extra_fields):
        """
        创建超级管理员
        """
        user = self.create_user(phone, name, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    """
    用户模型
    """
    name = models.CharField(max_length=255, verbose_name='姓名')
    phone = models.CharField(max_length=20, unique=True, verbose_name='手机号')
    password = models.CharField(max_length=128, verbose_name='密码')
    is_active = models.BooleanField(default=True, verbose_name='是否激活')
    date_joined = models.DateTimeField(default=timezone.now, verbose_name='加入时间')
    role = models.ForeignKey('Role', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='角色')
    is_staff = models.BooleanField(default=False, verbose_name='是否为员工')

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['name']

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'

    def __str__(self):
        return f"{self.name} ({self.phone})"
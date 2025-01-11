from rest_framework import permissions
from .serializers import UserSerializer
from .permissions import IsAdminUserCustom

from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from .serializers import LoginSerializer
from .models import User
from utils.response import success_response, error_response


class LoginView(generics.GenericAPIView):
    """
    用户登录视图，返回JWT令牌、角色、菜单信息和用户姓名
    """
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]  # 允许任何未认证用户访问登录接口

    def post(self, request, *args, **kwargs):
        """
        处理用户登录请求，返回JWT令牌、角色、菜单信息和用户姓名
        """
        # 获取请求数据
        data = request.data.copy()
        serializer = self.get_serializer(data=data)

        # 校验序列化器
        if serializer.is_valid():
            # 获取手机号和密码
            phone = serializer.validated_data['phone']
            password = serializer.validated_data['password']

            # 使用自定义认证后端进行验证
            user = authenticate(request, phone=phone, password=password)

            if user is not None:
                # 登录成功，生成JWT令牌
                refresh = RefreshToken.for_user(user)

                # 获取用户角色的菜单权限
                menus = self.get_user_menus(user)

                # 返回JWT令牌、角色、菜单信息和用户姓名
                return success_response(
                    data={
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                        'role': user.role.name,  # 角色名称
                        'menus': menus,  # 角色菜单
                        'name': user.name  # 用户姓名
                    },
                    message="登录成功"
                )
            else:
                return error_response(message="手机号或密码错误", code=1001)

        # 如果序列化器无效，返回错误信息
        return error_response(message="参数错误", code=1002)

    def get_user_menus(self, user):
        """
        根据用户角色获取对应的菜单权限
        """
        role_menus = user.role.rolemenu_set.all()  # 获取角色与菜单的关系
        menus = []

        # 遍历角色与菜单关系，构建菜单列表
        for role_menu in role_menus:
            for menu in role_menu.menu.all():
                menus.append({
                    "title": menu.title,
                    "route": menu.route
                })

        return menus


class UserListView(generics.ListAPIView):
    """
    用户列表视图
    仅允许管理员用户访问
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUserCustom]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return success_response(data=serializer.data, message="查询成功", total=queryset.count())


class UserCreateView(generics.CreateAPIView):
    """
    创建用户视图
    仅允许管理员用户访问
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUserCustom]

    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            success_message = "用户创建成功！"
            return success_response(data=response.data, message=success_message, code=200)
        except Exception as e:
            return error_response(message="用户创建失败", code=1002, data=str(e))

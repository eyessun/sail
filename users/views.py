# users/views.py

from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken

class AdminLoginView(generics.GenericAPIView):
    """
    管理员登录视图
    """
    serializer_class = LoginSerializer

    def post(self, request):
        """
        处理管理员登录请求，返回JWT令牌
        """
        data = request.data.copy()
        data['role'] = 'admin'  # 强制角色为管理员
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        # 生成JWT刷新令牌和访问令牌
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)

class StaffLoginView(generics.GenericAPIView):
    """
    普通用户（业务员）登录视图
    """
    serializer_class = LoginSerializer

    def post(self, request):
        """
        处理普通用户登录请求，返回JWT令牌
        """
        data = request.data.copy()
        data['role'] = 'normal'  # 强制角色为普通用户
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        # 生成JWT刷新令牌和访问令牌
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)

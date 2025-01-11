# users/urls.py

from django.urls import path
# from .views import AdminLoginView, StaffLoginView

from .views import (
    LoginView,
    UserListView,
    UserCreateView,
)

urlpatterns = [
    path('login/', LoginView.as_view(), name='admin_login'),  # 管理员登录

    # 用户管理
    path('userslist/', UserListView.as_view(), name='admin-user-list'),

    # 创建用户
    path('create/', UserCreateView.as_view(), name='staff-user-list'),

]

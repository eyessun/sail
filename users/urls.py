# users/urls.py

from django.urls import path
from .views import AdminLoginView, StaffLoginView

urlpatterns = [
    path('admin/login/', AdminLoginView.as_view(), name='admin_login'),  # 管理员登录
    path('staff/login/', StaffLoginView.as_view(), name='staff_login'),  # 普通用户登录
]

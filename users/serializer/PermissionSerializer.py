from rest_framework import serializers
from ..models import Permission

class PermissionSerializer(serializers.ModelSerializer):
    """
    权限序列化器：用于展示每个权限的详细信息。
    """
    class Meta:
        model = Permission
        fields = ['id', 'name', 'description']
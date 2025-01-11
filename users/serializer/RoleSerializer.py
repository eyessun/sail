from rest_framework import serializers
from ..models import Role
from . import PermissionSerializer

class RoleSerializer(serializers.ModelSerializer):
    """
    角色序列化器：用于展示角色信息及其拥有的权限。
    """

    class Meta:
        model = Role
        fields = ['id', 'name', 'permissions']
from rest_framework import serializers
from django.contrib.auth import get_user_model
from apps.admin.models import (
    Role,
    Permission,
    SystemSetting,
    AdminSetting,
    AdminAuditLog,
)

User = get_user_model()

class AdminUserSerializer(serializers.ModelSerializer):
    role = serializers.StringRelatedField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "is_active",
            "is_staff",
            "is_superuser",
            "role",
        ]


class AdminUserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "is_staff",
        ]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ["id", "code", "description"]

class RoleSerializer(serializers.ModelSerializer):
    permissions = serializers.ListField(
        child=serializers.CharField(),
        allow_empty=True
    )

    class Meta:
        model = Role
        fields = ["id", "name", "permissions"]


class SystemSettingSerializer(serializers.ModelSerializer):
    updated_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = SystemSetting
        fields = "__all__"
        read_only_fields = ("updated_by", "updated_at")

class AdminSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminSetting
        fields = "__all__"

class AdminAuditLogSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = AdminAuditLog
        fields = [
            "id",
            "user",
            "action",
            "resource",
            "metadata",
            "timestamp",
        ]

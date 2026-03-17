""" from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class AdminUserSerializer(serializers.ModelSerializer):
    
    READ (list/detail) and UPDATE (partial=True).
    Password is write-only — never returned in responses.
    
    full_name    = serializers.SerializerMethodField()
    role_display = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "full_name",
            "phone",
            "role",
            "role_display",
            "is_active",
            "is_staff",
            "is_superuser",
            "date_joined",
            "last_login",
            "password",
        ]
        read_only_fields = [
            "id", "date_joined", "last_login", "full_name", "role_display"
        ]
        extra_kwargs = {
            "password": {"write_only": True, "required": False}
        }

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip() or obj.username

    def get_role_display(self, obj):
        return obj.get_role_display() if hasattr(obj, "get_role_display") else obj.role

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class AdminUserCreateSerializer(serializers.ModelSerializer):
    
    POST /api/admin/users/ only.
    Admin can assign ANY role — unlike public RegisterSerializer (defaults client).
    Password required, min 8 chars.
    
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "phone",
            "role",
            "is_active",
            "password",
        ]
        extra_kwargs = {
            "role":      {"required": True},
            "is_active": {"default": True},
            "phone":     {"required": False, "allow_blank": True},
        }

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                "A user with this username already exists."
            )
        return value

    def validate_email(self, value):
        if value and User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "A user with this email already exists."
            )
        return value

    def validate_role(self, value):
        valid_roles = [r[0] for r in User.ROLE_CHOICES]
        if value not in valid_roles:
            raise serializers.ValidationError(
                f"Invalid role. Choose from: {', '.join(valid_roles)}"
            )
        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user """

from rest_framework import serializers
from django.contrib.auth import get_user_model
from apps.admin.models import (
    Role,
    AdminAuditLog,
    Permission,
    PermissionMatrix,
    SystemSetting,
    AdminSetting,
)

User = get_user_model()


# ════════════════════════════════════════════
# USER SERIALIZERS
# ════════════════════════════════════════════

class AdminUserSerializer(serializers.ModelSerializer):
    """READ (list/detail) and UPDATE (partial=True)."""
    full_name    = serializers.SerializerMethodField()
    role_display = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id", "username", "email", "first_name", "last_name",
            "full_name", "phone", "role", "role_display",
            "is_active", "is_staff", "is_superuser",
            "date_joined", "last_login", "password",
        ]
        read_only_fields = [
            "id", "date_joined", "last_login", "full_name", "role_display"
        ]
        extra_kwargs = {"password": {"write_only": True, "required": False}}

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip() or obj.username

    def get_role_display(self, obj):
        return dict(User.ROLE_CHOICES).get(obj.role, obj.role)

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class AdminUserCreateSerializer(serializers.ModelSerializer):
    """POST /api/admin/users/ — admin picks any role."""
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = [
            "username", "email", "first_name", "last_name",
            "phone", "role", "is_active", "password",
        ]
        extra_kwargs = {
            "role":      {"required": True},
            "is_active": {"default": True},
            "phone":     {"required": False, "allow_blank": True},
            "email":     {"required": True},
        }

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with this username already exists.")
        return value

    def validate_email(self, value):
        if value and User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate_role(self, value):
        valid_roles = [r[0] for r in User.ROLE_CHOICES]
        if value not in valid_roles:
            raise serializers.ValidationError(
                f"Invalid role. Choose from: {', '.join(valid_roles)}"
            )
        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


# ════════════════════════════════════════════
# ROLE SERIALIZER
# ════════════════════════════════════════════

class RoleSerializer(serializers.ModelSerializer):
    """Serializer for the Role model."""
    user_count = serializers.SerializerMethodField()

    class Meta:
        model = Role
        fields = ["id", "name", "permissions", "user_count"]

    def get_user_count(self, obj):
        # Count users whose role string matches this Role name
        return User.objects.filter(role=obj.name.lower().replace(" ", "_")).count()


# ════════════════════════════════════════════
# AUDIT LOG SERIALIZER
# ════════════════════════════════════════════

class AdminAuditLogSerializer(serializers.ModelSerializer):
    """Serializer for AdminAuditLog model."""
    user     = serializers.StringRelatedField()
    username = serializers.SerializerMethodField()

    class Meta:
        model = AdminAuditLog
        fields = [
            "id", "user", "username", "action",
            "resource", "metadata", "timestamp",
        ]
        read_only_fields = fields

    def get_username(self, obj):
        return obj.user.username if obj.user else "System"


# ════════════════════════════════════════════
# PERMISSION SERIALIZERS
# ════════════════════════════════════════════

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ["id", "code", "description"]


class PermissionMatrixSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermissionMatrix
        fields = ["id", "role", "permission", "allowed"]


# ════════════════════════════════════════════
# SETTINGS SERIALIZERS
# ════════════════════════════════════════════

class SystemSettingSerializer(serializers.ModelSerializer):
    updated_by = serializers.StringRelatedField()

    class Meta:
        model = SystemSetting
        fields = ["id", "key", "value", "description", "updated_by", "updated_at"]
        read_only_fields = ["id", "updated_at", "updated_by"]


class AdminSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminSetting
        fields = ["id", "key", "value", "updated_at"]
        read_only_fields = ["id", "updated_at"]
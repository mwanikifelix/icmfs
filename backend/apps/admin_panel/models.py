from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


class Permission(models.Model):
    code = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.code


class SystemSetting(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.JSONField()
    description = models.TextField(blank=True)

    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL
    )
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.key


class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)
    permissions = models.JSONField(default=list)

    def __str__(self):
        return self.name


class AdminAuditLog(models.Model):
    ACTION_CHOICES = (
        ("CREATE", "Create"),
        ("UPDATE", "Update"),
        ("DELETE", "Delete"),
        ("LOGIN", "Login"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL
    )
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    resource = models.CharField(max_length=100)
    metadata = models.JSONField(default=dict, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} {self.action} {self.resource}"


class AdminSetting(models.Model):

    key = models.CharField(max_length=100, unique=True)
    value = models.JSONField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.key


class PermissionMatrix(models.Model):
    role = models.CharField(max_length=100)
    permission = models.CharField(max_length=100)
    allowed = models.BooleanField(default=True)

    class Meta:
        unique_together = ("role", "permission")

    def __str__(self):
        return f"{self.role} → {self.permission}"

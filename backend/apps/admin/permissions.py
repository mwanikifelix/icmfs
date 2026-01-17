# apps/admin/permissions.py
from rest_framework.permissions import BasePermission
from apps.admin.models import PermissionMatrix


class IsDjangoSuperAdmin(BasePermission):
    """
    For internal emergency access (Django admin level)
    """

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.is_staff
            and request.user.is_superuser
        )


class IsSystemAdmin(BasePermission):
    """
    Role-based system admin (ICMFS)
    """

    def has_permission(self, request, view):
        user = request.user

        return (
            user
            and user.is_authenticated
            and (
                user.is_superuser
                or user.is_staff
                or user.role == "System Admin"
            )
        )


class HasICMFSPermission(BasePermission):
    """
    Fine-grained permission via PermissionMatrix
    """

    def has_permission(self, request, view):
        user = request.user
        required_permission = getattr(view, "required_permission", None)

        # No permission required → allow
        if not required_permission:
            return True

        if not user or not user.is_authenticated:
            return False

        role = getattr(user, "role", None)
        if not role:
            return False

        return PermissionMatrix.objects.filter(
            role=role.name,
            permission=required_permission,
            allowed=True,
        ).exists()

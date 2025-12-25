""" # apps/admin_panel/permissions.py
from rest_framework.permissions import BasePermission


class IsSystemAdmin(BasePermission):


    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.is_staff
            and request.user.is_superuser
        )


class IsSystemAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and hasattr(request.user, "role")
            and request.user.role        
            and request.user.role.name == "System Admin"
        ) """


from rest_framework.permissions import BasePermission


class IsSystemAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and getattr(request.user, "role", None)
            and request.user.role.name == "SystemAdmin"
        )


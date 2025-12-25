from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminManagerOrOwner(BasePermission):
    """
    Allows access only to:
    - Admins
    - Project Managers
    - Object owner
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        user = request.user

        if user.role in ["admin", "manager"]:
            return True

        return hasattr(obj, "owner") and obj.owner == user

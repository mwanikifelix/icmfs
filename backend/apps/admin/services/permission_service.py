from apps.admin.models import PermissionMatrix


def has_permission(role_name, permission_code):
    return PermissionMatrix.objects.filter(
        role=role_name,
        permission=permission_code,
        allowed=True,
    ).exists()

# apps/admin/services/audit.py

from apps.admin.models import AdminAuditLog


def log_action(*, user, action, resource, metadata=None):
    """
    Centralized admin audit logger.
    """
    AdminAuditLog.objects.create(
        user=user,
        action=action,
        resource=resource,
        metadata=metadata or {},
    )

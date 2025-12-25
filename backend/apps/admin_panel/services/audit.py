import logging
from apps.admin_panel.models import AdminAuditLog

logger = logging.getLogger(__name__)

def log_admin_action(user, action, resource, metadata=None):
    AdminAuditLog.objects.create(
        user=user,
        action=action,
        resource=resource,
        metadata=metadata or {},
    )
    logger.info(f"{user} | {action} | {resource}")

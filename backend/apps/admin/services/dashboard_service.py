from django.contrib.auth import get_user_model

from apps.admin.models import AdminAuditLog
from apps.admin.services.permission_service import has_permission
from apps.admin.services.cache_service import cached
from apps.admin.services.project_service import get_project_metrics
from apps.admin.services.finance_service import get_finance_metrics
from apps.admin.services.time_analytics_service import (
    users_by_month,
    projects_by_month,
    finance_by_month,
    audit_activity_by_week,
)

User = get_user_model()


# ----------------------------
# RAW DASHBOARD METRICS
# (NEVER role-filtered here)
# ----------------------------
def get_dashboard_metrics():
    return {
        "users": {
            "total": User.objects.count(),
            "active": User.objects.filter(is_active=True).count(),
            "staff": User.objects.filter(is_staff=True).count(),
            "admins": User.objects.filter(is_superuser=True).count(),
        },
        "projects": get_project_metrics(),
        "finance": get_finance_metrics(),
        "audit": {
            "total_logs": AdminAuditLog.objects.count(),
            "recent": list(
                AdminAuditLog.objects.order_by("-timestamp")
                .values("action", "resource", "timestamp")[:5]
            ),
        },
    }


def get_time_based_metrics():
    return {
        "users_by_month": list(users_by_month()),
        "projects_by_month": list(projects_by_month()),
        "finance_by_month": list(finance_by_month()),
        "audit_by_week": list(audit_activity_by_week()),
    }


# ----------------------------
# CACHED RAW METRICS
# ----------------------------
def get_dashboard_metrics_cached():
    return cached(
        key="admin_dashboard_metrics",
        fn=get_dashboard_metrics,
        timeout=60,
    )


def get_time_based_metrics_cached():
    return cached(
        key="admin_time_metrics",
        fn=get_time_based_metrics,
        timeout=120,
    )


# ----------------------------
# ROLE-BASED FILTERING
# (APPLIED PER REQUEST)
# ----------------------------
def filter_metrics_for_role(metrics, time_metrics, role_name):
    """
    Enforce PermissionMatrix on dashboard data.
    """
    if not role_name:
        return {}

    filtered = {}

    if has_permission(role_name, "VIEW_USERS"):
        filtered["users"] = metrics.get("users")
        filtered["users_by_month"] = time_metrics.get("users_by_month")

    if has_permission(role_name, "VIEW_PROJECTS"):
        filtered["projects"] = metrics.get("projects")
        filtered["projects_by_month"] = time_metrics.get("projects_by_month")

    if has_permission(role_name, "VIEW_FINANCE"):
        filtered["finance"] = metrics.get("finance")
        filtered["finance_by_month"] = time_metrics.get("finance_by_month")

    if has_permission(role_name, "VIEW_AUDIT"):
        filtered["audit"] = metrics.get("audit")
        filtered["audit_by_week"] = time_metrics.get("audit_by_week")

    return filtered

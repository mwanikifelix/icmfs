# apps/admin/urls.py

from django.urls import path

from apps.admin.views.dashboard import AdminDashboardView, AdminPanelIndexView
from apps.admin.views.analytics import AdminAnalyticsView
from apps.admin.views.users import AdminUserListView
from apps.admin.views.roles import AdminRoleListView
from apps.admin.views.settings import AdminSettingsView
from apps.admin.views.audit_logs import AdminAuditLogListView
from apps.admin.views.permissions_matrix import PermissionMatrixView

urlpatterns = [
    # Root → Dashboard
    path("", AdminDashboardView.as_view(), name="admin-dashboard"),
    

    # Core admin modules
    path("analytics/", AdminAnalyticsView.as_view(), name="admin-analytics"),
    path("users/", AdminUserListView.as_view(), name="admin-users"),
    path("roles/", AdminRoleListView.as_view(), name="admin-roles"),
    path("settings/", AdminSettingsView.as_view(), name="admin-settings"),
    path("analytics/", AdminAnalyticsView.as_view()),
    path("audit-logs/", AdminAuditLogListView.as_view()),
    path("permissions-matrix/", PermissionMatrixView.as_view()),

    path("", AdminPanelIndexView.as_view(), name="admin-index"),
    path("dashboard/", AdminDashboardView.as_view(), name="admin-dashboard"),
    path("audit/", AdminAuditLogListView.as_view(), name="admin-audit"),


    # Security & governance
    path("audit-logs/", AdminAuditLogListView.as_view(), name="admin-audit-logs"),
    path(
        "permissions-matrix/",
        PermissionMatrixView.as_view(),
        name="admin-permission-matrix",
    ),
]

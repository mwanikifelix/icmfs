"""from django.urls import path

from apps.admin_panel.views.roles import AdminRoleListView
from apps.admin_panel.views.dashboard import AdminDashboardView
from apps.admin_panel.views.permissions import AdminPermissionView

from apps.admin_panel.views.settings import (
    AdminSettingsView,
    AdminSettingsDetailView,
)
from apps.admin_panel.views.users import (
    AdminUserListView,
    AdminUserCreateView,
    AdminUserDetailView,
)

urlpatterns = [
    path("settings/", AdminSettingsView.as_view(), name="admin-settings"),
    path("settings/<int:pk>/", AdminSettingsDetailView.as_view(), name="admin-setting-detail"),

    path("dashboard/", AdminDashboardView.as_view()),
    path("users/", AdminUserListView.as_view()),
    path("roles/", AdminRoleListView.as_view()),
    path("permissions/", AdminPermissionView.as_view()),
    path("settings/", AdminSettingsView.as_view()),



    path("users/", AdminUserListView.as_view(), name="admin-users"),
    path("users/create/", AdminUserCreateView.as_view(), name="admin-user-create"),
    path("users/<int:pk>/", AdminUserDetailView.as_view(), name="admin-user-detail"),
]
"""

# apps/admin_panel/urls.py

from django.urls import path
from apps.admin_panel.views.settings import AdminSettingsView
from apps.admin_panel.views.audit_logs import AdminAuditLogListView
from apps.admin_panel.services.audit import log_admin_action
from apps.admin_panel.views.permissions_matrix import PermissionMatrixView

from apps.admin_panel.views.dashboard import AdminDashboardView
from apps.admin_panel.views.users import AdminUserListView
from apps.admin_panel.views.roles import AdminRoleListView

urlpatterns = [
    path("dashboard/", AdminDashboardView.as_view(), name="admin-dashboard"),
    path("users/", AdminUserListView.as_view(), name="admin-users"),
    path("settings/", AdminSettingsView.as_view(), name="admin-settings"),
    path("audit-logs/", AdminAuditLogListView.as_view(), name="admin-audit-logs"),
    path(
        "permissions-matrix/", PermissionMatrixView.as_view(), name="permission-matrix"
    ),
    path("roles/", AdminRoleListView.as_view(), name="admin-roles"),
]

""" from django.urls import path

from apps.admin.views.dashboard import AdminDashboardView, AdminPanelIndexView
from apps.admin.views.analytics import AdminAnalyticsView
from apps.admin.views.audit_logs import AdminAuditLogListView
from apps.admin.views.permissions_matrix import PermissionMatrixView
from apps.admin.views.roles import AdminRoleListView
from apps.admin.views.settings import AdminSettingsView
from apps.admin.views.users import (
    AdminUserListView,
    AdminUserDetailView,
    AdminUserResetPasswordView,
    AdminUserToggleStatusView,
    AdminUserStatsView,
)

urlpatterns = [

    # ── Dashboard ──────────────────────────────────────────────
    path("",           AdminDashboardView.as_view(),  name="admin-index"),
    path("dashboard/", AdminDashboardView.as_view(),  name="admin-dashboard"),

    # ── Users ──────────────────────────────────────────────────
    path("users/",                         AdminUserListView.as_view(),          name="admin-users"),
    path("users/stats/",                   AdminUserStatsView.as_view(),         name="admin-user-stats"),
    path("users/<int:pk>/",                AdminUserDetailView.as_view(),        name="admin-user-detail"),
    path("users/<int:pk>/reset-password/", AdminUserResetPasswordView.as_view(), name="admin-user-reset-password"),
    path("users/<int:pk>/toggle-status/",  AdminUserToggleStatusView.as_view(),  name="admin-user-toggle-status"),

    # ── Roles ──────────────────────────────────────────────────
    path("roles/",              AdminRoleListView.as_view(),      name="admin-roles"),

    # ── Audit ──────────────────────────────────────────────────
    path("audit/",              AdminAuditLogListView.as_view(),  name="admin-audit"),
    path("audit-logs/",         AdminAuditLogListView.as_view(),  name="admin-audit-logs"),

    # ── Analytics ──────────────────────────────────────────────
    path("analytics/",          AdminAnalyticsView.as_view(),     name="admin-analytics"),

    # ── Settings ───────────────────────────────────────────────
    path("settings/",           AdminSettingsView.as_view(),      name="admin-settings"),

    # ── Permissions matrix ─────────────────────────────────────
    path("permissions-matrix/", PermissionMatrixView.as_view(),   name="admin-permission-matrix"),
] """




from django.urls import path

from apps.admin.views.dashboard import AdminDashboardView, AdminPanelIndexView
from apps.admin.views.analytics import AdminAnalyticsView
from apps.admin.views.audit_logs import AdminAuditLogListView
from apps.admin.views.permissions_matrix import PermissionMatrixView
from apps.admin.views.roles import AdminRoleListView
from apps.admin.views.settings import AdminSettingsView
from apps.admin.views.users import (
    AdminUserListView,
    AdminUserDetailView,
    AdminUserResetPasswordView,
    AdminUserToggleStatusView,
    AdminUserStatsView,
)

urlpatterns = [

    # ── Dashboard ──────────────────────────────────────────────
    path("",           AdminDashboardView.as_view(),  name="admin-index"),
    path("dashboard/", AdminDashboardView.as_view(),  name="admin-dashboard"),

    # ── Users ──────────────────────────────────────────────────
    path("users/",                         AdminUserListView.as_view(),          name="admin-users"),
    path("users/stats/",                   AdminUserStatsView.as_view(),         name="admin-user-stats"),
    path("users/<int:pk>/",                AdminUserDetailView.as_view(),        name="admin-user-detail"),
    path("users/<int:pk>/reset-password/", AdminUserResetPasswordView.as_view(), name="admin-user-reset-password"),
    path("users/<int:pk>/toggle-status/",  AdminUserToggleStatusView.as_view(),  name="admin-user-toggle-status"),

    # ── Roles ──────────────────────────────────────────────────
    path("roles/",              AdminRoleListView.as_view(),      name="admin-roles"),

    # ── Audit ──────────────────────────────────────────────────
    path("audit/",              AdminAuditLogListView.as_view(),  name="admin-audit"),
    path("audit-logs/",         AdminAuditLogListView.as_view(),  name="admin-audit-logs"),

    # ── Analytics ──────────────────────────────────────────────
    path("analytics/",          AdminAnalyticsView.as_view(),     name="admin-analytics"),

    # ── Settings ───────────────────────────────────────────────
    path("settings/",           AdminSettingsView.as_view(),      name="admin-settings"),

    # ── Permissions matrix ─────────────────────────────────────
    path("permissions-matrix/", PermissionMatrixView.as_view(),   name="admin-permission-matrix"),
]
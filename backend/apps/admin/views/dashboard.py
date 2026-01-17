from rest_framework.views import APIView
from rest_framework.response import Response

from apps.admin.permissions import IsSystemAdmin
from apps.admin.services.system import system_info
from apps.admin.services.dashboard_service import (
    get_dashboard_metrics_cached,
    get_time_based_metrics_cached,
    filter_metrics_for_role,
)


class AdminPanelIndexView(APIView):
    """
    Lightweight health & counts endpoint
    (used for quick checks, sidebar badges, ping tests)
    """
    permission_classes = [IsSystemAdmin]

    def get(self, request):
        return Response(
            {
                "status": "ok",
                "message": "Admin panel operational",
            }
        )


class AdminDashboardView(APIView):
    """
    Main admin dashboard endpoint
    (used for dashboard cards, charts, summaries)
    """
    permission_classes = [IsSystemAdmin]

    def get(self, request):
        role_name = request.user.role


        analytics = get_dashboard_metrics_cached()
        time_series = get_time_based_metrics_cached()

        return Response(
            {
                "status": "ok",
                "system": system_info(),
                "analytics": filter_metrics_for_role(analytics, role_name),
                "time_series": time_series,
            }
        )

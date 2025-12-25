from rest_framework.views import APIView
from rest_framework.response import Response
from apps.admin_panel.permissions import IsSystemAdmin
from apps.accounts.models import User
from apps.projects.models import Project
from apps.admin_panel.services.system import system_info


class AdminPanelIndexView(APIView):
    permission_classes = [IsSystemAdmin]

    def get(self, request):
        return Response({
            "users": User.objects.count(),
            "projects": Project.objects.count(),
            "status": "Admin panel operational"
        })


class AdminDashboardView(APIView):
    permission_classes = [IsSystemAdmin]

    def get(self, request):
        return Response({
            "status": "ok",
            "message": "Admin Panel is running",
            "system": system_info()
        })
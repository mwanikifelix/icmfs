from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django.contrib.auth import get_user_model
from apps.admin_panel.models import AdminAuditLog

User = get_user_model()


class AdminAnalyticsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        return Response({
            "users": {
                "total": User.objects.count(),
                "active": User.objects.filter(is_active=True).count(),
                "staff": User.objects.filter(is_staff=True).count(),
                "admins": User.objects.filter(is_superuser=True).count(),
            },
            "audit_logs": {
                "total": AdminAuditLog.objects.count(),
            }
        })

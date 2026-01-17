from rest_framework.views import APIView
from rest_framework.response import Response

from django.contrib.auth import get_user_model

from apps.admin.permissions import IsSystemAdmin
from apps.admin.models import AdminAuditLog

User = get_user_model()


class AdminAnalyticsView(APIView):
    permission_classes = [IsSystemAdmin]

    def get(self, request):
        users_qs = User.objects.all()

        data = {
            "users": {
                "total": users_qs.count(),
                "active": users_qs.filter(is_active=True).count(),
                "staff": users_qs.filter(is_staff=True).count(),
                "admins": users_qs.filter(is_superuser=True).count(),
            },
            "audit_logs": {
                "total": AdminAuditLog.objects.count(),
            },
        }

        return Response(data)

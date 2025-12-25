from rest_framework.views import APIView
from rest_framework.response import Response

from apps.admin_panel.models import AdminAuditLog
from apps.admin_panel.serializers import AdminAuditLogSerializer
from apps.admin_panel.permissions import IsSystemAdmin


class AdminAuditLogListView(APIView):
    permission_classes = [IsSystemAdmin]

    def get(self, request):
        logs = AdminAuditLog.objects.all()[:500]  # safety limit
        serializer = AdminAuditLogSerializer(logs, many=True)
        return Response(serializer.data)

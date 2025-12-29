from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from apps.admin_panel.permissions import IsAdmin
from apps.admin_panel.models import AdminAuditLog
from apps.admin_panel.serializers import AdminAuditLogSerializer


class AdminAuditLogListView(ListAPIView):
    queryset = AdminAuditLog.objects.select_related("user").order_by("-created_at")
    serializer_class = AdminAuditLogSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

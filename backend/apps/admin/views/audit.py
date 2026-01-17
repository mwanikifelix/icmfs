""" from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from apps.admin.models import AdminAuditLog


class AdminAuditLogListView(APIView):

    

    permission_classes = [IsAdminUser]

    def get(self, request):
        logs = AdminAuditLog.objects.select_related("user").order_by("-created_at")[:100]

        data = [
            {
                "id": log.id,
                "user": log.user.username if log.user else None,
                "action": log.action,
                "resource": log.resource,
                "metadata": log.metadata,
                "created_at": log.created_at,
            }
            for log in logs
        ]

        return Response(
            {
                "count": len(data),
                "results": data,
            }
        )
 """

from rest_framework.views import APIView
from rest_framework.response import Response

from apps.admin.models import AdminAuditLog
from apps.admin.permissions import IsSystemAdmin


class AdminAuditLogListView(APIView):
    permission_classes = [IsSystemAdmin]

    def get(self, request):
        logs = AdminAuditLog.objects.select_related("user").order_by("-id")[:100]

        results = []
        for log in logs:
            results.append({
                "id": log.id,
                "user": log.user.username if log.user else "system",
                "action": log.action,
                "resource": log.resource,
                "created_at": getattr(log, "created_at", None)
                    or getattr(log, "timestamp", None),
                "metadata": log.metadata,
            })

        return Response({
            "count": len(results),
            "results": results,
        })


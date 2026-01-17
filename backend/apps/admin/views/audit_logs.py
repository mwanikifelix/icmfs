from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination

from apps.admin.models import AdminAuditLog
from apps.admin.serializers import AdminAuditLogSerializer
from apps.admin.permissions import IsSystemAdmin


class AdminAuditLogPagination(LimitOffsetPagination):
    default_limit = 50
    max_limit = 500


class AdminAuditLogListView(APIView):
    permission_classes = [IsSystemAdmin]
    pagination_class = AdminAuditLogPagination

    def get(self, request):
        queryset = AdminAuditLog.objects.all().order_by("-timestamp")

        # Optional filters (safe & useful)
        action = request.query_params.get("action")
        user = request.query_params.get("user")

        if action:
            queryset = queryset.filter(action=action)

        if user:
            queryset = queryset.filter(user__username__icontains=user)

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)

        serializer = AdminAuditLogSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

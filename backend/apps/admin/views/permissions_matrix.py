from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.admin.models import PermissionMatrix
from apps.admin.permissions import IsSystemAdmin
from apps.admin.services.audit import log_action


class PermissionMatrixView(APIView):
    permission_classes = [IsSystemAdmin]

    def get(self, request):
        data = list(
            PermissionMatrix.objects.all().values(
                "id", "role", "permission", "allowed"
            )
        )
        return Response(data)

    def post(self, request):
        role = request.data.get("role")
        permission = request.data.get("permission")
        allowed = request.data.get("allowed")

        if role is None or permission is None or allowed is None:
            return Response(
                {"detail": "role, permission and allowed are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        obj, _ = PermissionMatrix.objects.update_or_create(
            role=role,
            permission=permission,
            defaults={"allowed": bool(allowed)},
        )

        # audit log (CRITICAL for ICMFS)
        log_action(
            user=request.user,
            action="UPDATE",
            resource="PERMISSION_MATRIX",
            metadata={
                "role": role,
                "permission": permission,
                "allowed": bool(allowed),
            },
        )

        return Response(
            {
                "status": "updated",
                "role": obj.role,
                "permission": obj.permission,
                "allowed": obj.allowed,
            }
        )

from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Inspection
from .serializers import InspectionSerializer
from apps.notifications.services import send_notification


class InspectionViewSet(viewsets.ModelViewSet):
    queryset = Inspection.objects.all()
    serializer_class = InspectionSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=["post"])
    def approve(self, request, pk=None):
        inspection = self.get_object()
        inspection.status = "approved"
        inspection.save()

        return Response({"status": "approved"})

    @action(detail=True, methods=["post"])
    def reject(self, request, pk=None):
        inspection = self.get_object()
        inspection.status = "rejected"
        inspection.save()

        # 🔔 Notify engineer on rejection
        send_notification(
            user=inspection.progress.created_by,
            title="QA Inspection Rejected",
            message="Rework required on submitted progress",
            notification_type="alert",
        )

        return Response({"status": "rejected"})

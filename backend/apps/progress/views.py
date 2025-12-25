from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import EVMSnapshotSerializer
from apps.progress.services.evm import EVMService
from apps.progress.models import EVMSnapshot, DailyProgress
from apps.notifications.services import send_notification

from .serializers import DailyProgressSerializer
from .services import evaluate_evm_risk


class DailyProgressViewSet(viewsets.ModelViewSet):
    queryset = DailyProgress.objects.all()
    serializer_class = DailyProgressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        progress = serializer.save(created_by=self.request.user)
        project = progress.project

        # 🔔 Notify Project Manager
        if project.manager:
            send_notification(
                user=project.manager,
                title="New Daily Progress Submitted",
                message=f"Progress submitted for {project.name}",
                notification_type="info",
            )

        # 📊 Run EVM Risk Evaluation
        evaluate_evm_risk(project)

    @action(detail=True, methods=["post"])
    def approve(self, request, pk=None):
        progress = self.get_object()
        progress.status = "approved"
        progress.save()

        return Response({"status": "approved"})

    @action(detail=True, methods=["post"])
    def reject(self, request, pk=None):
        progress = self.get_object()
        progress.status = "rejected"
        progress.save()

        # 🔔 Notify Engineer on rejection
        send_notification(
            user=progress.created_by,
            title="QA Inspection Rejected",
            message="Rework required on submitted progress",
            notification_type="alert",
        )

        return Response({"status": "rejected"})


@action(detail=True, methods=["post"])
def approve(self, request, pk=None):
    progress = self.get_object()
    project = progress.project

    progress.status = "approved"
    progress.approved_by = request.user
    progress.save()

    evm = EVMService(project)

    pv = evm.planned_value()
    ac = evm.actual_cost()
    ev = evm.earned_value(progress.percent_complete)

    cpi = evm.cpi(ev, ac)
    spi = evm.spi(ev, pv)
    eac = evm.eac(cpi)
    etc = evm.etc(eac, ac)

    EVMSnapshot.objects.create(
        project=project,
        progress=progress,
        pv=pv,
        ev=ev,
        ac=ac,
        cpi=cpi,
        spi=spi,
        eac=eac,
        etc=etc,
    )

    # 🔔 Risk notification (Affordable Housing Critical)
    if cpi < 0.9 or spi < 0.9:
        send_notification(
            user=project.owner,
            title="Project At Risk",
            message="EVM metrics indicate cost or schedule overrun",
            notification_type="warning",
        )

    return Response({"status": "Progress approved & EVM calculated"})


class EVMSnapshotViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only EVM metrics per project
    """

    queryset = EVMSnapshot.objects.all().order_by("-created_at")
    serializer_class = EVMSnapshotSerializer
    permission_classes = [IsAuthenticated]

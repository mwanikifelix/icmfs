from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import FinancialRecord, Payment
from .serializers import FinancialRecordSerializer, PaymentSerializer
from .services import calculate_evm
from apps.projects.models import Project


class FinancialRecordViewSet(ModelViewSet):
    queryset = FinancialRecord.objects.all()
    serializer_class = FinancialRecordSerializer
    permission_classes = [IsAuthenticated]


class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]


class EVMViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=["get"])
    def summary(self, request, pk=None):
        project = Project.objects.get(pk=pk)
        evm = calculate_evm(project)
        return Response(evm)

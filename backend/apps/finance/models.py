from django.db import models
from django.conf import settings
from apps.projects.models import Project
from apps.progress.models import DailyProgress
import uuid


class FinancialRecord(models.Model):
    """
    Represents Actual Cost (AC) entries
    """

    id = models.BigAutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="financial_records"
    )

    progress = models.ForeignKey(
        DailyProgress,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="financial_links"
    )

    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=14, decimal_places=2)

    recorded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )

    recorded_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.project.name} - {self.amount}"


class Payment(models.Model):
    """
    Represents outgoing or incoming payments
    """

    PAYMENT_STATUS = (
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("rejected", "Rejected"),
    )

    id = models.BigAutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="payments"
    )

    amount = models.DecimalField(max_digits=14, decimal_places=2)
    reference = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default="pending")

    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    payment_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.project.name} - {self.status}"

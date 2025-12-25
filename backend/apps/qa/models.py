from django.db import models
from django.conf import settings
from apps.projects.models import Project
from apps.progress.models import DailyProgress
import uuid


class Inspection(models.Model):
    """
    QA/QC inspection for construction works
    """

    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
        ("rework", "Rework Required"),
    )

    id = models.BigAutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="inspections"
    )

    progress = models.ForeignKey(
        DailyProgress,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="qa_inspections",
    )

    title = models.CharField(max_length=200)
    remarks = models.TextField(blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    inspected_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="qa_reviews",
    )

    inspected_at = models.DateTimeField(auto_now_add=True)

    signed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.project.name} - {self.status}"

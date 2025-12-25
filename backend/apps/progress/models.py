from django.db import models
from django.conf import settings
from apps.projects.models import Project


class DailyProgress(models.Model):
    id = models.BigAutoField(primary_key=True)

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="daily_reports"
    )

    reported_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="progress_reports"
    )

    report_date = models.DateField()

    work_done_description = models.TextField()

    planned_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Planned % completion for the day"
    )

    actual_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Actual % completion achieved"
    )

    actual_cost = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        help_text="Actual cost incurred for the day (KES)"
    )

    approved = models.BooleanField(default=False)

    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approved_progress_reports"
    )

    approved_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("project", "report_date")
        ordering = ["-report_date"]

    def __str__(self):
        return f"{self.project.name} - {self.report_date}"

    # -------------------------
    # EVM COMPUTATION HOOKS
    # -------------------------
    def planned_value(self):
        if self.project.budget:
            return (self.planned_percentage / 100) * self.project.budget
        return 0

    def earned_value(self):
        if self.project.budget:
            return (self.actual_percentage / 100) * self.project.budget
        return 0

    def cost_performance_index(self):
        ev = self.earned_value()
        if self.actual_cost > 0:
            return ev / self.actual_cost
        return 0

    def schedule_performance_index(self):
        pv = self.planned_value()
        ev = self.earned_value()
        if pv > 0:
            return ev / pv
        return 0


class EVMSnapshot(models.Model):
    project = models.ForeignKey(
        "projects.Project",
        on_delete=models.CASCADE,
        related_name="evm_snapshots"
    )
    progress = models.ForeignKey(
        "progress.DailyProgress",
        on_delete=models.CASCADE,
        related_name="evm_snapshots"
    )

    pv = models.DecimalField(max_digits=15, decimal_places=2)
    ev = models.DecimalField(max_digits=15, decimal_places=2)
    ac = models.DecimalField(max_digits=15, decimal_places=2)

    cpi = models.DecimalField(max_digits=8, decimal_places=2)
    spi = models.DecimalField(max_digits=8, decimal_places=2)

    eac = models.DecimalField(max_digits=15, decimal_places=2)
    etc = models.DecimalField(max_digits=15, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

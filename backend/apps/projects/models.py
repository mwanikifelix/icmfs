import uuid
from django.db import models
from django.conf import settings
from apps.accounts.models import AbstractUser

User = settings.AUTH_USER_MODEL


class Project(models.Model):
    id = models.BigAutoField(primary_key=True)

    name = models.CharField(max_length=255)

    # Project Owner / Sponsor (Client)
    sponsor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="owned_projects",
        limit_choices_to={"role": "CLIENT"},
        help_text="Client / Project Owner",
    )

    STATUS_CHOICES = [
        ("planned", "Planned"),
        ("active", "Active"),
        ("on_hold", "On Hold"),
        ("at_risk", "At Risk"),
        ("completed", "Completed"),
        ("closed", "Closed"),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="planned")

    budget = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Approved project budget (KES)",
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_projects",
    )

    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "projects"

    def __str__(self):
        return self.name


class ProjectSite(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="sites")
    site_name = models.CharField(max_length=255)
    county = models.CharField(max_length=100)
    town = models.CharField(max_length=100, blank=True)
    gps_latitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )
    gps_longitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )
    status = models.CharField(max_length=20, default="active")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.site_name


class ProjectMember(models.Model):
    ROLE_CHOICES = (
        ("engineer", "Engineer"),
        ("architect", "Architect"),
        ("consultant", "Consultant"),
        ("accountant", "Accountant"),
        ("manager", "Project Manager"),
        ("owner", "Owner"),
    )

    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="members"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES)
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("project", "user")


class ProjectWBS(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="wbs_items"
    )
    wbs_code = models.CharField(max_length=50)
    wbs_name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    planned_cost = models.DecimalField(max_digits=15, decimal_places=2)
    planned_start = models.DateField()
    planned_end = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("project", "wbs_code")

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ("system_admin", "System Admin"),
        ("admin", "Admin"),
        ("manager", "Project Manager"),
        ("engineer", "Engineer"),
        ("qa", "QA/QC"),
        ("finance", "Finance"),
        ("client", "Client"),
    )

    phone = models.CharField(max_length=20, blank=True)
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="client",
    )

    is_active = models.BooleanField(default=True)

    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return f"{self.username} ({self.role})"

from django.db import models
from django.conf import settings
import uuid


class Notification(models.Model):
    """
    System-wide notifications
    """

    NOTIFICATION_TYPE = (
        ("info", "Info"),
        ("warning", "Warning"),
        ("alert", "Alert"),
    )

    id = models.BigAutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications"
    )

    title = models.CharField(max_length=200)
    message = models.TextField()

    notification_type = models.CharField(
        max_length=20, choices=NOTIFICATION_TYPE, default="info"
    )

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} → {self.user.username}"

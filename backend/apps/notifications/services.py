from .models import Notification


def send_notification(
    *,
    user,
    title,
    message,
    notification_type="info"
):
    """
    Central notification sender
    """
    Notification.objects.create(
        user=user,
        title=title,
        message=message,
        notification_type=notification_type,
    )

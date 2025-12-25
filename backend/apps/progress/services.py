# apps/progress/services.py

from apps.notifications.services import send_notification


def evaluate_evm_risk(project):
    """
    Check CPI/SPI and raise alerts
    """
    if project.cpi < 0.9 or project.spi < 0.9:
        project.status = "at_risk"
        project.save()

        # 🔔 NOTIFY PROJECT OWNER
        send_notification(
            user=project.owner,
            title="Project At Risk",
            message="EVM metrics indicate cost or schedule overrun",
            notification_type="warning",
        )

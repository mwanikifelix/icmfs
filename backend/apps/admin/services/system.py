from apps.admin.models import SystemSetting


def get_setting(key, default=None):
    try:
        return SystemSetting.objects.get(key=key).value
    except SystemSetting.DoesNotExist:
        return default


def set_setting(key, value, description=""):
    setting, _ = SystemSetting.objects.update_or_create(
        key=key,
        defaults={
            "value": value,
            "description": description,
        },
    )
    return setting


def system_info():
    return {"system": "ICMFS", "version": "1.0.0", "maintenance": False}

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings

from apps.admin.models import (
    Role,
    SystemSetting,
    PermissionMatrix,
    AdminSetting,
    AdminAuditLog,
)


def _log(action, instance):
    AdminAuditLog.objects.create(
        user=getattr(instance, "updated_by", None),
        action=action,
        resource=instance.__class__.__name__,
        metadata={
            "id": instance.pk,
        },
    )


@receiver(post_save, sender=Role)
def role_saved(sender, instance, created, **kwargs):
    _log("CREATE" if created else "UPDATE", instance)


@receiver(post_save, sender=SystemSetting)
def system_setting_saved(sender, instance, created, **kwargs):
    _log("CREATE" if created else "UPDATE", instance)


@receiver(post_save, sender=PermissionMatrix)
def permission_matrix_saved(sender, instance, created, **kwargs):
    _log("CREATE" if created else "UPDATE", instance)


@receiver(post_delete, sender=Role)
@receiver(post_delete, sender=SystemSetting)
@receiver(post_delete, sender=PermissionMatrix)
def critical_object_deleted(sender, instance, **kwargs):
    _log("DELETE", instance)

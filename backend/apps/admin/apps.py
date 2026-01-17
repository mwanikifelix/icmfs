from django.apps import AppConfig


class AdminConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.admin"
    label = "ICMFS_admin"          # ✅ REQUIRED (must be unique)
    verbose_name = "ICMFS Admin Panel"

    def ready(self):
        import apps.admin.signals  # noqa

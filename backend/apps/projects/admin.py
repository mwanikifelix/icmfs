from django.contrib import admin
from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "sponsor",
        "status",
        "budget",
        "start_date",
        "end_date",
        "created_at",
    )

    list_filter = ("status",)
    search_fields = ("name", "sponsor__username", "sponsor__email")

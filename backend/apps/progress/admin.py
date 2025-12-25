from django.contrib import admin
from .models import DailyProgress


@admin.register(DailyProgress)
class DailyProgressAdmin(admin.ModelAdmin):
    list_display = (
        "project",
        "report_date",
        "planned_percentage",
        "actual_percentage",
        "actual_cost",
        "approved",
    )

    list_filter = ("approved", "report_date")
    search_fields = ("project__name",)

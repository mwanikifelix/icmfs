from django.contrib.auth import get_user_model
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth, TruncWeek

from apps.projects.models import Project
from apps.finance.models import FinancialRecord
from apps.admin.models import AdminAuditLog

User = get_user_model()


def users_by_month():
    return (
        User.objects.annotate(month=TruncMonth("date_joined"))
        .values("month")
        .annotate(count=Count("id"))
        .order_by("month")
    )


def projects_by_month():
    return (
        Project.objects.annotate(month=TruncMonth("created_at"))
        .values("month")
        .annotate(count=Count("id"))
        .order_by("month")
    )


def finance_by_month():
    return (
        FinancialRecord.objects.annotate(month=TruncMonth("recorded_date"))
        .values("month")
        .annotate(total=Sum("amount"))
        .order_by("month")
    )


def audit_activity_by_week():
    return (
        AdminAuditLog.objects.annotate(week=TruncWeek("timestamp"))
        .values("week")
        .annotate(count=Count("id"))
        .order_by("week")
    )

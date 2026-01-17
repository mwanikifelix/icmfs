from apps.finance.models import FinancialRecord
from django.db.models import Sum


def get_finance_metrics():
    """
    Financial dashboard metrics
    """
    total_amount = (
        FinancialRecord.objects.aggregate(total=Sum("amount"))["total"] or 0
    )

    return {
        "records": FinancialRecord.objects.count(),
        "total_amount": float(total_amount),
    }

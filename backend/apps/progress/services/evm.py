from decimal import Decimal, InvalidOperation
from apps.finance.models import FinancialRecord
from apps.projects.models import Project
from django.db.models import Sum


class EVMService:
    def __init__(self, project: Project):
        self.project = project

    def planned_value(self):
        """
        PV = Budget at Completion (BAC)
        """
        return Decimal(self.project.budget)

    def actual_cost(self):
        """
        AC = Sum of approved finance records
        """
        total = FinancialRecord.objects.filter(
            project=self.project,
            status="approved"
        ).aggregate(sum=models.Sum("amount"))["sum"] or 0

        return Decimal(total)

    def earned_value(self, percent_complete):
        """
        EV = PV * % complete
        """
        pv = self.planned_value()
        return (Decimal(percent_complete) / Decimal(100)) * pv

    def cpi(self, ev, ac):
        """
        CPI = EV / AC
        """
        try:
            return ev / ac if ac > 0 else Decimal(0)
        except (InvalidOperation, ZeroDivisionError):
            return Decimal(0)

    def spi(self, ev, pv):
        """
        SPI = EV / PV
        """
        try:
            return ev / pv if pv > 0 else Decimal(0)
        except (InvalidOperation, ZeroDivisionError):
            return Decimal(0)

    def eac(self, cpi):
        """
        EAC = BAC / CPI
        """
        try:
            return self.planned_value() / cpi if cpi > 0 else self.planned_value()
        except (InvalidOperation, ZeroDivisionError):
            return self.planned_value()

    def etc(self, eac, ac):
        """
        ETC = EAC - AC
        """
        return eac - ac

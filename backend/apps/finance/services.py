from decimal import Decimal


def calculate_evm(project):
    """
    Computes EAC and ETC
    """

    total_ac = sum(
        [record.amount for record in project.financial_records.all()], Decimal("0.00")
    )

    ev = project.ev or Decimal("0.00")  # earned value
    bac = project.budget_at_completion

    if ev > 0:
        cpi = ev / total_ac if total_ac > 0 else Decimal("0.00")
        eac = bac / cpi if cpi > 0 else bac
    else:
        eac = bac

    etc = eac - total_ac

    return {
        "AC": total_ac,
        "EAC": round(eac, 2),
        "ETC": round(etc, 2),
    }

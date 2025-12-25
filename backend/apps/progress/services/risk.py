def evaluate_evm_risk(cpi: float, spi: float) -> str:
    """
    Evaluate project risk based on EVM indicators.
    """
    if cpi < 0.9 or spi < 0.9:
        return "high"
    elif cpi < 1.0 or spi < 1.0:
        return "medium"
    return "low"

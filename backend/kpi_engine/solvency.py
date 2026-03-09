def debt_to_equity(total_debt: float, total_equity: float) -> float:
    if total_equity == 0:
        return 0.0
    return total_debt / total_equity

def debt_ratio(total_debt: float, total_assets: float) -> float:
    if total_assets == 0:
        return 0.0
    return total_debt / total_assets

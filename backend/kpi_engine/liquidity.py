def current_ratio(current_assets: float, current_liabilities: float) -> float:
    if current_liabilities == 0:
        return 0.0
    return current_assets / current_liabilities

def quick_ratio(current_assets: float, inventory: float, current_liabilities: float) -> float:
    if current_liabilities == 0:
        return 0.0
    return (current_assets - inventory) / current_liabilities

def safe_div(numerator, denominator):
    try:
        if numerator is None or denominator in [0, None]:
            return None
        return float(numerator) / float(denominator)
    except:
        return None


def current_ratio(current_assets: float, current_liabilities: float):
    return safe_div(current_assets, current_liabilities)


def quick_ratio(current_assets: float, inventory: float, current_liabilities: float):
    if inventory is None:
        inventory = 0
    return safe_div(current_assets - inventory, current_liabilities)
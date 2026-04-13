def safe_div(numerator, denominator):
    try:
        if numerator is None or denominator in [0, None]:
            return None
        return float(numerator) / float(denominator)
    except:
        return None


def debt_to_equity(total_debt: float, total_equity: float):
    return safe_div(total_debt, total_equity)


def debt_ratio(total_debt: float, total_assets: float):
    return safe_div(total_debt, total_assets)
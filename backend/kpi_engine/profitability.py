def safe_div(numerator, denominator):
    try:
        if numerator is None or denominator in [0, None]:
            return None
        return float(numerator) / float(denominator)
    except:
        return None


def net_profit_margin(net_income: float, revenue: float):
    result = safe_div(net_income, revenue)
    return result * 100 if result is not None else None


def return_on_assets(net_income: float, total_assets: float):
    result = safe_div(net_income, total_assets)
    return result * 100 if result is not None else None


def return_on_equity(net_income: float, equity: float):
    result = safe_div(net_income, equity)
    return result * 100 if result is not None else None
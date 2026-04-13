def safe_div(numerator, denominator):
    try:
        if numerator is None or denominator in [0, None]:
            return None
        return float(numerator) / float(denominator)
    except:
        return None


def asset_turnover(revenue: float, total_assets: float):
    return safe_div(revenue, total_assets)
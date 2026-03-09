import pandas as pd

def calculate_net_profit_margin(net_income: float, revenue: float) -> float:
    if revenue == 0:
        return 0.0
    return (net_income / revenue) * 100

def calculate_roa(net_income: float, total_assets: float) -> float:
    if total_assets == 0:
        return 0.0
    return (net_income / total_assets) * 100

def calculate_roe(net_income: float, shareholders_equity: float) -> float:
    if shareholders_equity == 0:
        return 0.0
    return (net_income / shareholders_equity) * 100

def net_profit_margin(net_income, revenue):
    if revenue == 0:
        return 0
    return (net_income / revenue) * 100


def return_on_assets(net_income, total_assets):
    if total_assets == 0:
        return 0
    return (net_income / total_assets) * 100
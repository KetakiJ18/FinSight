import pandas as pd
from io import BytesIO

def load_csv(file_bytes: bytes) -> pd.DataFrame:
    try:
        df = pd.read_csv(BytesIO(file_bytes))
        return df
    except Exception as e:
        raise ValueError(f"Error loading CSV: {e}")

def detect_file_type(df: pd.DataFrame) -> str:
    """
    Attempts to identify the type of financial statement based on column names.
    This is a naive implementation; expand as needed.
    """
    columns = [str(c).lower() for c in df.columns]
    
    if any("revenue" in c or "sales" in c or "net income" in c for c in columns):
        return "profit_and_loss"
    elif any("asset" in c or "liabilit" in c or "equity" in c for c in columns):
        return "balance_sheet"
    elif any("cash flow" in c or "operating activities" in c for c in columns):
        return "cash_flow"
        
    return "unknown"

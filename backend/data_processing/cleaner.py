import pandas as pd
import re

def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans a pandas DataFrame by standardizing column names, dropping empty rows,
    and handling common missing values.
    """
    cleaned_df = df.copy()
    
    cleaned_df.columns = [clean_column_name(c) for c in cleaned_df.columns]
    
    cleaned_df.dropna(how='all', inplace=True)
    
    # Do not fill numeric NaNs with 0; keep as NaN for proper handling
    return cleaned_df

def clean_column_name(col_name: str) -> str:
    """
    Normalizes a column name to lowercase, alphanumeric characters, and underscores.
    e.g., "Net Income ($)" -> "net_income"
    """
    if not isinstance(col_name, str):
        return str(col_name)
    
    cleaned = re.sub(r'[^a-zA-Z0-9\s]', '', col_name)
    cleaned = re.sub(r'\s+', '_', cleaned.strip())
    
    return cleaned.lower()

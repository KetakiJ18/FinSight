import pandas as pd
from typing import Dict

def merge_datasets(dataframes: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """
    Merges multiple financial statements (P&L, Balance Sheet, Cash Flow) into a single
    structured dataset. 
    Assumes standard structured DataFrames with a common index or 'year' column.
    """
    if not dataframes:
        return pd.DataFrame()
        
    merged_df = None
    
    for label, df in dataframes.items():
        date_cols = [col for col in df.columns if 'year' in col.lower() or 'date' in col.lower()]
        merge_key = date_cols[0] if date_cols else None
        
        if merged_df is None:
            merged_df = df
        else:
            if merge_key and merge_key in merged_df.columns:
                merged_df = pd.merge(merged_df, df, on=merge_key, how='outer', suffixes=('', f'_{label}'))
            else:
                # If no merge key, concatenate and handle duplicates
                merged_df = pd.concat([merged_df, df], axis=1, ignore_index=False)
    
    # Remove duplicate columns after merge
    merged_df = merged_df.loc[:, ~merged_df.columns.duplicated()]
    
    return merged_df

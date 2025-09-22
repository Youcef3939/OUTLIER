import pandas as pd
from sklearn.preprocessing import StandardScaler

def clean_missing(df: pd.DataFrame, strategy='mean') -> pd.DataFrame:
    """Fill missing values in the DataFrame."""
    for col in df.columns:
        if df[col].dtype in ['float64', 'int64']:
            if strategy == 'mean':
                df[col] = df[col].fillna(df[col].mean())
            elif strategy == 'median':
                df[col] = df[col].fillna(df[col].median())
        else:
            df[col] = df[col].fillna(df[col].mode()[0])
    return df

def scale_numeric(df: pd.DataFrame, numeric_cols: list) -> pd.DataFrame:
    """Standardize numeric columns."""
    df[numeric_cols] = StandardScaler().fit_transform(df[numeric_cols])
    return df

if __name__ == "__main__":
    from data_loader import load_data

    # Load sample dataset
    df = load_data("../data/sample.csv")
    print("Original DataFrame:")
    print(df)

    # Clean missing values
    df_clean = clean_missing(df)
    print("\nAfter cleaning missing values:")
    print(df_clean)

    # Scale numeric columns
    numeric_cols = ["value1", "value2"]
    df_scaled = scale_numeric(df_clean, numeric_cols)
    print("\nAfter scaling numeric columns:")
    print(df_scaled)

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor


def detect_zscore(df: pd.DataFrame, threshold: float = 3.0) -> pd.DataFrame:
    """Detect outliers using Z-score method."""
    z_scores = np.abs((df - df.mean()) / df.std())
    outliers = (z_scores > threshold)
    return outliers.any(axis=1)  # type: ignore

def detect_iqr(df: pd.DataFrame, k: float = 1.5) -> pd.DataFrame:
    """Detect outliers using IQR method."""
    Q1 = df.quantile(0.25)
    Q3 = df.quantile(0.75)
    IQR = Q3 - Q1
    outliers = ((df < (Q1 - k * IQR)) | (df > (Q3 + k * IQR)))
    return outliers.any(axis=1) # type: ignore

def detect_isolation_forest(df: pd.DataFrame, contamination: float = 0.05) -> pd.DataFrame:
    """Detect outliers using Isolation Forest."""
    model = IsolationForest(contamination=contamination, random_state=42)
    preds = model.fit_predict(df)
    # -1 indicates outlier
    return pd.Series(preds == -1, index=df.index) # type: ignore

def detect_lof(df: pd.DataFrame, n_neighbors: int = 20) -> pd.DataFrame:
    """Detect outliers using Local Outlier Factor (LOF)."""
    model = LocalOutlierFactor(n_neighbors=n_neighbors, contamination=0.05)
    preds = model.fit_predict(df)
    # -1 indicates outlier
    return pd.Series(preds == -1, index=df.index) # type: ignore


if __name__ == "__main__":
    from data_loader import load_data
    from preprocessing import clean_missing, scale_numeric

    df = load_data("../data/sample.csv")

    df_clean = clean_missing(df)
    numeric_cols = ["value1", "value2"]
    df_scaled = scale_numeric(df_clean, numeric_cols)

    print("\nZ-score outliers:")
    print(detect_zscore(df_scaled[numeric_cols]))

    print("\nIQR outliers:")
    print(detect_iqr(df_scaled[numeric_cols]))

    print("\nIsolation Forest outliers:")
    print(detect_isolation_forest(df_scaled[numeric_cols]))

    print("\nLOF outliers:")
    print(detect_lof(df_scaled[numeric_cols]))
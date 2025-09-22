import pandas as pd
import numpy as np
import os

def explain_outliers_combined(df_original, df_scaled, methods_masks):
    """
    Generate human-friendly explanations for outliers detected by multiple methods,
    combining all methods per row into a single explanation.

    Parameters:
        df_original (DataFrame): Original unscaled dataframe
        df_scaled (DataFrame): Scaled dataframe used for detection
        methods_masks (dict): {method_name: boolean_series_of_outliers}
    Returns:
        DataFrame: Columns ["row_index", "explanation"]
    """
    all_outlier_indices = set()
    for mask in methods_masks.values():
        all_outlier_indices.update(df_scaled.index[mask])
    
    explanations = []

    for idx in sorted(all_outlier_indices):
        row_parts = []
        for method_name, mask in methods_masks.items():
            if mask[idx]:
                col_parts = []
                for col in df_original.columns:
                    val = df_original.at[idx, col]
                    mean = df_original[col].mean()
                    std = df_original[col].std()
                    if std == 0:
                        continue
                    deviation = (val - mean) / std
                    if abs(deviation) > 1:
                        direction = "higher" if deviation > 0 else "lower"
                        col_parts.append(f"{col} = {val} ({direction} than typical)")
                if col_parts:
                    row_parts.append(f"{method_name}: " + ", ".join(col_parts))
        explanation_text = f"Row {idx+1} was detected as an outlier because: " + "; ".join(row_parts) + "."
        explanations.append({"row_index": idx+1, "explanation": explanation_text})

    return pd.DataFrame(explanations)


if __name__ == "__main__":
    from data_loader import load_data
    from preprocessing import clean_missing, scale_numeric
    from detection import detect_zscore, detect_iqr, detect_isolation_forest, detect_lof

    df_original = load_data("../data/sample.csv")
    df_clean = clean_missing(df_original)
    numeric_cols = ["value1", "value2"]
    df_original_numeric = df_clean[numeric_cols].copy()
    df_scaled = scale_numeric(df_clean, numeric_cols)

    methods_masks = {
        "Z-score": detect_zscore(df_scaled[numeric_cols]),
        "IQR": detect_iqr(df_scaled[numeric_cols]),
        "Isolation Forest": detect_isolation_forest(df_scaled[numeric_cols]),
        "LOF": detect_lof(df_scaled[numeric_cols])
    }

    combined_df = explain_outliers_combined(df_original_numeric, df_scaled[numeric_cols], methods_masks)

    os.makedirs("../reports", exist_ok=True)
    report_path = "../reports/outlier_explanations_combined.csv"
    combined_df.to_csv(report_path, index=False)
    print(f"Combined human-friendly outlier report saved to: {report_path}")

    print("\nSample combined explanations:")
    for _, row in combined_df.head(3).iterrows():
        print(row["explanation"])

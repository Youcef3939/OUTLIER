import streamlit as st
import pandas as pd
import numpy as np
import sys, os
import plotly.express as px

SRC_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
sys.path.insert(0, SRC_PATH)

from main import run_outlier_detection

st.set_page_config(page_title="OUTLIER 🚨", layout="wide")
st.title("🚨 OUTLIER: Catch What Others Miss")

uploaded_file = st.file_uploader("Upload your CSV dataset", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("### Data Preview")
    st.dataframe(df.head())

    methods = st.sidebar.multiselect(
        "Select anomaly detection methods",
        ["Z-Score", "IQR", "Isolation Forest", "LOF"],
        default=["Z-Score", "IQR"]
    )

    z_thresh = st.sidebar.slider("Z-Score Threshold", 1.0, 5.0, 3.0, 0.1)
    iqr_factor = st.sidebar.slider("IQR Factor", 1.0, 3.0, 1.5, 0.1)
    iso_contamination = st.sidebar.slider("Isolation Forest Contamination", 0.01, 0.2, 0.05, 0.01)
    lof_neighbors = st.sidebar.slider("LOF Neighbors", 5, 50, 20, 1)
    likelihood_filter = st.sidebar.slider("Show anomalies with likelihood ≥ %", 0, 100, 0, 5)

    max_normal_points = 5000  

    if st.button("Run Detection"):
        results, plots = run_outlier_detection(
            df,
            methods=methods,
            z_thresh=z_thresh,
            iqr_factor=iqr_factor,
            iso_contamination=iso_contamination,
            lof_neighbors=lof_neighbors
        )

        if results.empty:
            st.info("No anomalies detected with the selected methods and thresholds.")
        else:
            temp = results.copy()
            agg_results = temp.groupby(temp.index).agg({
                **{col:'first' for col in df.columns},  
                'Method': lambda x: ', '.join(x),
                'Explanation': lambda x: ' | '.join(x)
            })

            agg_results['OUTLIER_Likelihood_%'] = agg_results['Method'].apply(
                lambda x: round(len(x.split(',')) / len(methods) * 100, 1)
            )

            filtered_results = agg_results[agg_results['OUTLIER_Likelihood_%'] >= likelihood_filter]

            def highlight_likelihood(row):
                if row['OUTLIER_Likelihood_%'] >= 75:
                    return ['background-color: #ff9999']*len(row)
                elif row['OUTLIER_Likelihood_%'] >= 50:
                    return ['background-color: #ffe599']*len(row)
                else:
                    return ['']*len(row)

            st.write("### Detected Anomalies")
            st.dataframe(filtered_results.style.apply(highlight_likelihood, axis=1))

            df_num = df.select_dtypes(include=[np.number]).astype(np.float32)

            for method in methods:
                mask_idx = results[results['Method'] == method].index
                anomaly_idx = df.index.intersection(mask_idx)
                normal_idx = df.index.difference(anomaly_idx)

                # Downsample normal points
                if len(normal_idx) > max_normal_points:
                    normal_sample = np.random.choice(normal_idx, max_normal_points, replace=False)
                else:
                    normal_sample = normal_idx

                plot_idx = np.concatenate([anomaly_idx, normal_sample])
                color_map = pd.Series(False, index=df.index)
                color_map[anomaly_idx] = True

                fig = px.scatter(
                    df_num.loc[plot_idx],
                    x=df_num.columns[0],
                    y=df_num.columns[1],
                    color=color_map.loc[plot_idx].map({True: "Anomaly", False: "Normal"}),
                    color_discrete_map={"Normal": "green", "Anomaly": "red"},
                    title=f"{method} Results"
                )
                st.plotly_chart(fig, use_container_width=True)

            high_likelihood_idx = filtered_results[filtered_results['OUTLIER_Likelihood_%'] >= 75].index
            mask_high = df.index.isin(high_likelihood_idx)
            normal_idx = df.index.difference(high_likelihood_idx)

            if len(normal_idx) > max_normal_points:
                normal_sample = np.random.choice(normal_idx, max_normal_points, replace=False)
            else:
                normal_sample = normal_idx

            plot_idx = np.concatenate([high_likelihood_idx, normal_sample])
            color_map = pd.Series(False, index=df.index)
            color_map[high_likelihood_idx] = True

            if len(high_likelihood_idx) > 0:
                fig = px.scatter(
                    df_num.loc[plot_idx],
                    x=df_num.columns[0],
                    y=df_num.columns[1],
                    color=color_map.loc[plot_idx].map({True: "High Likelihood Anomaly", False: "Normal"}),
                    color_discrete_map={"Normal": "green", "High Likelihood Anomaly": "orange"},
                    title="High Likelihood Anomalies (≥75%)"
                )
                st.plotly_chart(fig, use_container_width=True)

            report_df = filtered_results[filtered_results['OUTLIER_Likelihood_%'] >= 50].reset_index()
            report_df = report_df.rename(columns={'index': 'Row_ID'})
            report_df = report_df[['Row_ID', 'Method', 'OUTLIER_Likelihood_%', 'Explanation']]

            csv = report_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "Download Executive Report CSV",
                csv,
                "OUTLIER_report.csv",
                "text/csv",
                key="download-csv"
            )
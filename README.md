# OUTLIER 🚨 : catch what others miss

![alt text](image.png)

![Python](https://img.shields.io/badge/python-3.11-blue)
![outliers detected](https://img.shields.io/badge/outliers-🚨-red)
![Data Detective](https://img.shields.io/badge/Data%20Detective-%F0%9F%94%8D-yellow)
![AI](https://img.shields.io/badge/AI-🤖-blue)

**OUTLIER** isn't just another anomaly detector. it's your **digital watchdog**, trained to sniff out the rare, the weird and the suspicious and tell you **exactly why it raised the alarm**
 
think of it as having a superpowered lens over your data:

- spot a rogue trade in the stock market? done

- detect a failing sensor before disaster strikes? also done

- highlight suspicious patterns in server logs? surely done
 
OUTLIER doesn't just scream **something's wrong**, it whispers the story behind each anomaly:

> "point 42 is 3.4σ above the mean: outlier detected"


---

## features

- **explainable AI**: every anomaly comes with a reason

- **multiple detection engines**: Z-score, isolation forest, one-class SVM

- **built-in visualization**: spot anomalies in your data at a glance

- **plug & play**: works on time series, tabular datasets, or streams


---

## quickstart


# Clone & enter repo
```bash
git clone https://github.com/Youcef3939/OUTLIER.git

cd outlier
```
# Install dependencies
```
pip install -r requirements.txt
```

---

## example: detect & explain
```
from src.detector import OutlierDetector
from src.visualizer import plot_anomalies

detector = OutlierDetector(method="zscore", threshold=3.0)
results = detector.fit_predict(data)

for r in results:
    if r["is_anomaly"]:
        print(f"Index {r['index']} flagged: {r['reason']}")

plot_anomalies(data, results)
```

---

## the workflow

- data input

   - users can upload datasets in CSV, Excel, or directly fetch from APIs (e.g., financial data, sensor logs)

   - the system validates the data: checks for missing values, correct types, and proper formatting

- data preprocessing

   - missing values are handled (e.g., imputation or removal)

   - standardization or normalization is applied depending on the detection algorithm

   - categorical features are encoded if needed (one-hot, label encoding)

- outlier detection

  - multiple methods are available:

   - statistical: Z-score, IQR

   - machine learning: isolation forest, local outlier factor

- visualization & insights

   - outliers are visualized using interactive plots (histograms, scatter plots, box plots)

   - summary statistics are displayed: count of outliers, percentage, and severity

   - users can drill down to see specific outlier details

- export & reporting

   - users can download cleaned datasets or outlier reports


---

## diagram

```mermaid
flowchart TD

subgraph group_core["Core pipeline"]
  node_data_loader["Data loader<br/>ingest<br/>[data_loader.py]"]
  node_missing_values["Clean data<br/>preprocess step"]
  node_feature_scaling["Scale features<br/>preprocess step"]
  node_encoding["Encode data<br/>preprocess step"]
  node_detection_engine["Detector<br/>anomaly engine<br/>[detection.py]"]
  node_zscore["Z-score<br/>stat detector"]
  node_isoforest["Isolation Forest<br/>ml detector"]
  node_ocsvm["One-class SVM<br/>ml detector"]
  node_explainer["Explainer<br/>reasoning<br/>[explainer.py]"]
end

subgraph group_presentation["Presentation"]
  node_histogram["Histogram<br/>chart<br/>[visualization.py]"]
  node_scatter_plot["Scatter plot<br/>chart<br/>[visualization.py]"]
  node_box_plot["Box plot<br/>chart<br/>[visualization.py]"]
  node_dashboard_app["Dashboard<br/>interactive app<br/>[app.py]"]
end

subgraph group_data["Data"]
  node_sample_csv["Sample CSV<br/>sample input<br/>[sample.csv]"]
end

subgraph group_artifacts["Artifacts"]
  node_report_csv["Report CSV<br/>export"]
end

subgraph group_tests["Tests"]
  node_detector_tests["Detector tests<br/>test suite<br/>[test_detector.py]"]
end

node_sample_csv -->|"loads"| node_data_loader
node_dashboard_app -->|"starts"| node_data_loader
node_data_loader -->|"prepares"| node_missing_values
node_missing_values -->|"normalizes"| node_feature_scaling
node_feature_scaling -->|"encodes"| node_encoding
node_encoding -->|"feeds"| node_detection_engine
node_detection_engine -->|"runs"| node_zscore
node_detection_engine -->|"runs"| node_isoforest
node_detection_engine -->|"runs"| node_ocsvm
node_zscore -->|"flags"| node_explainer
node_isoforest -->|"flags"| node_explainer
node_ocsvm -->|"flags"| node_explainer
node_explainer -->|"visualizes"| node_histogram
node_explainer -->|"visualizes"| node_scatter_plot
node_explainer -->|"visualizes"| node_box_plot
node_explainer -->|"exports"| node_report_csv
node_dashboard_app -->|"surfaces"| node_explainer
node_dashboard_app -->|"renders"| node_histogram
node_dashboard_app -->|"renders"| node_scatter_plot
node_dashboard_app -->|"renders"| node_box_plot
node_detector_tests -.->|"verifies"| node_detection_engine

click node_sample_csv "https://github.com/youcef3939/outlier/blob/main/data/sample.csv"
click node_data_loader "https://github.com/youcef3939/outlier/blob/main/src/data_loader.py"
click node_detection_engine "https://github.com/youcef3939/outlier/blob/main/src/detection.py"
click node_explainer "https://github.com/youcef3939/outlier/blob/main/src/explainer.py"
click node_histogram "https://github.com/youcef3939/outlier/blob/main/src/visualization.py"
click node_scatter_plot "https://github.com/youcef3939/outlier/blob/main/src/visualization.py"
click node_box_plot "https://github.com/youcef3939/outlier/blob/main/src/visualization.py"
click node_dashboard_app "https://github.com/youcef3939/outlier/blob/main/dashboard/app.py"
click node_report_csv "https://github.com/youcef3939/outlier/blob/main/reports/outlier_explanations_combined.csv"
click node_detector_tests "https://github.com/youcef3939/outlier/blob/main/tests/test_detector.py"

classDef toneNeutral fill:#f8fafc,stroke:#334155,stroke-width:1.5px,color:#0f172a
classDef toneBlue fill:#dbeafe,stroke:#2563eb,stroke-width:1.5px,color:#172554
classDef toneAmber fill:#fef3c7,stroke:#d97706,stroke-width:1.5px,color:#78350f
classDef toneMint fill:#dcfce7,stroke:#16a34a,stroke-width:1.5px,color:#14532d
classDef toneRose fill:#ffe4e6,stroke:#e11d48,stroke-width:1.5px,color:#881337
classDef toneIndigo fill:#e0e7ff,stroke:#4f46e5,stroke-width:1.5px,color:#312e81
classDef toneTeal fill:#ccfbf1,stroke:#0f766e,stroke-width:1.5px,color:#134e4a
class node_data_loader,node_missing_values,node_feature_scaling,node_encoding,node_detection_engine,node_zscore,node_isoforest,node_ocsvm,node_explainer toneBlue
class node_histogram,node_scatter_plot,node_box_plot,node_dashboard_app toneAmber
class node_sample_csv toneMint
class node_report_csv toneRose
class node_detector_tests toneIndigo
```

---
## exemple output

![alt text](<Capture d'écran 2025-09-22 195442.png>)
![alt text](<Capture d'écran 2025-09-22 200244.png>)
![alt text](<Capture d'écran 2025-09-22 195740.png>)
![alt text](<Capture d'écran 2025-09-22 195810.png>)
![alt text](<Capture d'écran 2025-09-22 195825.png>)


---


## why OUTLIER?

because data doesn't lie, but it hides its secrets

OUTLIER is your key to uncovering them

whether you're a quant, engineer, researcher, or just a curious fella; if you want to spot the invisible patters, this is your tool!


---

## contributing

think you can spot a better anomaly? PRs are welcome!

open an issue first to discuss your idea

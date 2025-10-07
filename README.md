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

## 🧑‍💻 contributing

think you can spot a better anomaly? PRs are welcome!

open an issue first to discuss your idea

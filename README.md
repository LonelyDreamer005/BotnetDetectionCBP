# Botnet Detection & Classification (ML)

A machine learning pipeline that **detects** and **classifies** botnet traffic from network flow data using the CIC-DDoS2019 dataset.

## 🎯 What It Does
- **Detection**: Is this network traffic malicious or benign?
- **Classification**: What *type* of attack is it? (SYN Flood, LDAP Reflection)

## 📊 Results

| Class | Precision | Recall | F1-Score |
|:---|:---|:---|:---|
| **Benign** | 1.00 | 1.00 | 1.00 |
| **LDAP** | 1.00 | 1.00 | 1.00 |
| **Syn** | 1.00 | 1.00 | 1.00 |
| **UDP** | 1.00 | 1.00 | 1.00 |
| **Overall Accuracy** | | | **99.87%** |

## 🚀 Features
- **Multi-Class**: Classifies traffic as `Benign`, `Syn`, `LDAP`, or `UDP` (not just binary 0/1).
- **Real Dataset**: CIC-DDoS2019 (88,504 network flows across 6 Parquet files).
- **22 Behavioral Features**: Handpicked from 78 available columns (volume, timing, flags, rates).
- **Feature Importance**: Shows which network behaviors matter most for detection.
- **Model Export**: Saves trained classifier for deployment via `joblib`.

## 📁 Structure
- `Botnet_Detection.ipynb`: **Primary interactive notebook** with visualizations.
- `main.py`: CLI version of the pipeline.
- `data/`: SYN and LDAP training/testing Parquet files.
- `docs/`: In-depth explanations of the ML process.
- `results/`: Saved model, confusion matrix, and feature importance plots.

## 🛠️ Getting Started
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the CLI pipeline:
   ```bash
   python main.py
   ```
3. Or open `Botnet_Detection.ipynb` in Jupyter/VS Code.

## 🔬 Top Features for Detection
| Feature | Importance |
|:---|:---|
| Avg Packet Size | 0.1830 |
| ACK Flag Count | 0.1257 |
| Init Fwd Win Bytes | 0.1200 |
| Packet Length Mean | 0.0967 |
| Packet Length Std | 0.0915 |
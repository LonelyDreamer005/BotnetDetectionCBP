# Evaluation Metrics

Accuracy alone is not enough for cybersecurity projects. If 99% of traffic is benign, a model that simply predicts "Benign" every time would have 99% accuracy but would fail to detect any botnets.

## Key Metrics

### 1. Accuracy
- The percentage of correct predictions (both botnet and benign).
- `(TP + TN) / Total`

### 2. Precision
- Out of all samples predicted as **Botnet**, how many were actually botnets?
- High precision means fewer **False Alarms**.
- `TP / (TP + FP)`

### 3. Recall (Sensitivity)
- Out of all the **actual Botnets** in the data, how many did we catch?
- High recall means we didn't miss many attacks (**Low False Negatives**).
- `TP / (TP + FN)`

### 4. F1-Score
- The harmonic mean of Precision and Recall. It provides a single score that balances both.

## The Confusion Matrix (Security Perspective)

A table layout that allows visualization of performance by comparing Actual vs Predicted labels.

| Result | Security Meaning | Practical Consequence |
| :--- | :--- | :--- |
| **True Positive (TP)** | Botnet caught | **Success**: Attack blocked. |
| **True Negative (TN)** | Normal traffic allowed | **Success**: Business as usual. |
| **False Positive (FP)** | Normal flagged as Botnet | **False Alarm**: Annoyed users or blocked services. |
| **False Negative (FN)** | Botnet missed | **Security Breach**: Data loss or system hijack. |

> [!IMPORTANT]
> In cybersecurity, a **False Negative (FN)** is often considered much more dangerous than a **False Positive (FP)** because it represents a missed attack.

## Current Model Performance (SYN/LDAP)
| Metric | Score |
| :--- | :--- |
| **Accuracy** | **97.82%** |
| **Precision** | **0.98** |
| **Recall** | **0.98** |
| **F1-Score** | **0.98** |

### Confusion Matrix Highlights
*   **1641 Normals** correctly allowed.
*   **1629 Botnets** correctly caught.
*   Only **35 Botnets missed** (False Negatives).

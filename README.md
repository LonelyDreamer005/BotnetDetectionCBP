# 🛡️ Universal Botnet Detection & Classification

A state-of-the-art machine learning pipeline for detecting and classifying multi-class network botnet attacks using the **CIC-DDoS2019** dataset and cross-dataset validation.

---

## 🚀 Overview
This project evolves a standard binary detector into a **Universal Botnet Classifier**. It is designed not just to detect malicious activity, but to precisely identify the "Behavioral DNA" of specific attacks while remaining robust against laboratory artifacts and dataset bias.

### 🎯 Capability
- **Detection**: Identifies malicious vs. legitimate (Benign) traffic.
- **Classification**: Categorizes attacks into **SYN**, **LDAP**, and **UDP** floods.
- **Robustness**: Audited to ignore laboratory "cheat codes" and focus on flow behavior.
- **Generalization**: Validated against external datasets (`botnet_sample.csv`).

---

## 📊 Performance (Universal Model)
| Class | Precision | Recall | F1-Score |
|:---|:---|:---|:---|
| **Benign** | 1.00 | 1.00 | 1.00 |
| **Attack (SYN/LDAP/UDP)** | 1.00 | 1.00 | 1.00 |
| **Overall Accuracy** | | | **99.87%** |

---

## 📓 The Multi-Stage Workflow
The project is structured as 4 progressive laboratories to demonstrate the scientific process:

1. **[Main Lab](Botnet_Detection.ipynb)**: Building the 4-class detector.
2. **[Robustness Audit](Botnet_Detection_Robust.ipynb)**: Auditing for data leakage and laboratory artifacts.
3. **[Generalization Test](Botnet_Detection_Generalization.ipynb)**: Testing the model on completely unseen, external networks.
4. **[Universal Brain](Botnet_Detection_Universal.ipynb)**: Mixing multiple datasets to create a unified, robust classifier.

---

## 🐍 CLI Usage
You can train and evaluate the model directly from your terminal:

```bash
# Standard training (All features)
python main.py

# Hardened training (Drops suspicious laboratory artifacts)
python main.py --hardened
```

---

## 📖 Documentation & Guides
We have provided comprehensive guides for different levels of expertise:
- **[Ultra-Clear Summary](ULTRA_CLEAR_SUMMARY.md)**: A 2-minute visual roadmap of the project.
- **[Detailed Guide](DETAILED_GUIDE.md)**: A basic, conceptually focused explanation of "How it works."
- **[Technical Evolution](PROJECT_EXPLANATION.md)**: A deeper dive into the stages and technical challenges.
- **[Dataset Details](docs/dataset.md)**: Information on the CIC-DDoS2019 data.

---

## 🛠️ Technology Stack
- **Language**: Python 3.12+
- **Data**: Pandas, PyArrow (Parquet), NumPy
- **ML**: Scikit-Learn (Random Forest, StandardScaler)
- **Viz**: Matplotlib, Seaborn

---
**Maintained by**: Vinay
**Dataset Source**: [Canadian Institute for Cybersecurity (CIC)](https://www.unb.ca/cic/datasets/ddos-2019.html)
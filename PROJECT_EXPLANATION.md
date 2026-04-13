# Project Documentation: Botnet Detection and Multi-Class Classification

This document details the development of a multi-class botnet detection system, ranging from binary classification to a robust, network-agnostic universal classifier.

---

## 1. Project Objective
- **Primary Goal**: Development of a system capable of precise identification and categorization of network attack types.
- **Dataset**: Implementation utilizes the **CIC-DDoS2019** dataset, comprising real-world network traffic logs and diverse malicious behavior profiles.

---

## 2. Project Evolution and Phases

### Phase 1: Binary Classification
- **Scope**: Initial model development focused on distinguishing between **Benign** (normal) and **Attack** traffic.
- **Limitation**: Inability to differentiate between specific attack vectors (e.g., SYN flood vs. LDAP reflection).

### Phase 2: 3-Class Classification
- **Classification Categories**:
    1. **Benign**: Standard user traffic.
    2. **SYN Flood**: Direct TCP-based resource exhaustion.
    3. **LDAP Reflection**: Indirect UDP-based amplification attack.

### Phase 3: Data Integrity and Leakage Mitigation
- **Issue**: Identification of categorical discrepancies between original "Training" and "Testing" subsets. Disparity in feature processing (e.g., zero-value packet sizes in testing data) led to model degradation.
- **Resolution**: Integration of all available data followed by a **Stratified Split** to ensure consistent behavioral representation across training and evaluation sets.

### Phase 4: Final 4-Class Classification 
- **Expanded Scope**: Integration of **UDP Flooding** to complete the identification of primary botnet behaviors:
    1. **Benign** (Normal)
    2. **SYN** (Direct TCP)
    3. **LDAP** (Reflection UDP)
    4. **UDP** (Direct UDP)

---

## 3. Model Architecture and Methodology

### Random Forest Classifier
- **Configuration**: Implementation of a 200-decision tree ensemble.
- **Mechanism**: Aggregated voting from multiple estimators to achieve high-precision classification.

### Behavioral Feature Engineering
- **Selection**: 22 behavioral features selected to ensure resilience against IP spoofing.
- **Key Indicators**:
    - **Init Fwd Win Bytes**: Connection initialization behavior (critical for SYN detection).
    - **Average Packet Size**: Distinguishes between low-volume/high-frequency and high-volume traffic.
    - **Flag Counts**: Protocol adherence and state verification (TCP/UDP).

---

## 4. Performance Metrics
- **Accuracy**: 99.87%
- **Precision**: High confidence in attack type identification (low false positive rate for attack classes).
- **Recall**: High sensitivity in capturing malicious instances (low false negative rate).

---

## 5. Technical Components

### Model Development Notebooks
- **`Botnet_Detection.ipynb`**: Primary development environment for the 4-class classifier.
- **`Botnet_Detection_Robust.ipynb`**: Audit environment for feature leakage identification and behavioral intelligence validation.
- **`Botnet_Detection_Generalization.ipynb`**: Zero-shot testing environment utilizing external network traffic (`botnet_sample.csv`).
- **`Botnet_Detection_Universal.ipynb`**: Final integration stage utilizing multi-dataset fusion for universal application.

### Automation Tooling
- **`main.py`**: Command-line interface for automated data processing, model training, and serialization.
- **Output**: Trained models are serialized to `results/botnet_classifier.joblib`.

### Documentation Structure
- Detailed explanations for dataset selection, preprocessing techniques, training parameters, and evaluation results are located in the documentation repository.

---

**Summary**: The resulting security tool provides automated categorization of network botnet traffic with high-performance reliability across diverse network environments.

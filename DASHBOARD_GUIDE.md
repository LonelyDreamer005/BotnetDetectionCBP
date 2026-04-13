# Dashboard Technical Documentation: Botnet Detection UI

This guide details the visual components and technical narrative for the **Web Dashboard** (`app.py`).

## 🖥️ User Interface Structure

### 1. Stage Context (Left Panel)
Details the technical workflow of each development phase:
- **Phase Title**: Identification of the specific research stage.
- **Narrative**: Technical explanation of the methodology and rationale.
- **Concepts**: Highlights core techniques such as **Label Normalization**, **Leakage Mitigation**, and **Dataset Fusion**.

### 2. Experimental Output (Right Panel)
Displays metrics and data visualizations resulting from each stage:
- **Phase Metrics**: Provides statistical data including Accuracy, Algorithm type, Audit status, and Deployment type.
- **System Recall**: Security-focused metric tracking the model's performance in identifying malicious traffic.
- **Visualization Component**: Stage-specific Confusion Matrices and Feature Importance plots.

---

## 🛤️ Four-Stage Pipeline

### Stage 1: Multi-Class Classification
Initial training on the **CIC-DDoS2019** dataset utilizing 22 features and 4 labels. Baseline behavioral metrics established.

### Stage 2: Robustness Audit
Focuses on identification and mitigation of **Laboratory Leakage** (Identity Bytes). Model resilience enhanced by focusing on behavioral timing and volume features.

### Stage 3: Generalization Analysis
Stress-testing of the laboratory-trained model on unseen network traffic to measure the **Generalization Gap** and mitigate environmental bias.

### Stage 4: Universal Sentinel
Final developmental phase utilizing **Multi-Source Data Fusion**. Creation of a robust, network-agnostic detector for global application.

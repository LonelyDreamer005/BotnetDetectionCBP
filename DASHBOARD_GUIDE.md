# 📊 Botnet Detection Dashboard Guide

This guide explains the visual components and the technical narrative displayed in the **Web Dashboard** (`app.py`).

## 🖥️ UI Overview
The dashboard is split into two primary interactable sections:

### 1. Stage Context (Left Panel)
Displays the technical workflow of each development phase:
- **Title & Subtitle**: Identifies the specific focus of the research stage.
- **Narrative**: A concise, technical explanation of the "Why" and "How" for that stage.
- **Documentation Style**: Highlights key concepts like **Label Normalization**, **Leakage Mitigation**, and **Dataset Fusion**.

### 2. Experimental Output (Right Panel)
Displays the resulting metrics and visualizations:
- **Phase Metrics**: Provides unique statistics (Accuracy, Algorithm type, Audit status, or Deployment type).
- **System Recall**: A safety-focused metric tracking the model's ability to catch malicious traffic.
- **Visualization Chart**: Displaying Stage-specific Confusion Matrices or Feature Importance plots.

---

## 🛤️ The 4-Stage Journey

### Stage 1: Multi-Class Classification
Foundational training on the **CIC-DDoS2019** dataset using 22 features and 4 labels. Establish initial behavioral benchmarks.

### Stage 2: Robustness Audit
The "Reality Shield" phase. We audit the model for **Laboratory Leakage** (Identity Bytes) and harden it by focusing only on behavioral timing and volume.

### Stage 3: Generalization Test
The "Reality Check." We stress-test the lab-trained model on unseen network traffic. This stage highlights the **Generalization Gap** where models can become "blind" to external attack styles.

### Stage 4: Universal Brain
The final evolution. Using **Dataset Mixing**, we create a robust, network-agnostic sentinel that understands the universal language of DDoS regardless of the network environment.

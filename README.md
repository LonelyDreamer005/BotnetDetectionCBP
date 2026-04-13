# 🛡️ Universal Botnet Detection & Classification

Research-driven machine learning project to identify, audit, and neutralize DDoS/Botnet traffic using Behavioral AI.

## 🚀 Quick Start: Web Dashboard
To view interactive results and the 4-stage research journey:
1. **Dependency Installation**: `pip install flask pandas numpy scikit-learn joblib matplotlib seaborn pyarrow`
2. **Dashboard Execution**: `python app.py`
3. **Interface Access**: `http://localhost:5000`

---

## 🛤️ Four-Stage Research Pipeline
The project is structured as an evolutionary journey across 4 Core Notebooks:
1. **[Stage 1: Classification](Botnet_Detection.ipynb)**: Building the 4-class detector (99.8% Accuracy).
2. **[Stage 2: Audit](Botnet_Detection_Robust.ipynb)**: Identifying and removing "Laboratory Artifacts" (Leakage).
3. **[Stage 3: Cross-Test](Botnet_Detection_Generalization.ipynb)**: Stress-testing on unseen external datasets.
4. **[Stage 4: Universal Sentinel](Botnet_Detection_Universal.ipynb)**: Final robust detector trained on mixed global sources.

---

## 📖 Key Documentation
- **[Dashboard Technical Documentation](DASHBOARD_GUIDE.md)**: Detailed breakdown of the Dashboard UI.
- **[Technical Evolution Report](PROJECT_EXPLANATION.md)**: Conceptual deep-dive into the ML architecture.
- **[Project Roadmap](ULTRA_CLEAR_SUMMARY.md)**: Visual roadmap of the 4 stages.

---

## ⚙️ CLI Usage (Main Pipeline)
Headless training and automation via CLI:
```bash
# Hardened training (Drops laboratory artifacts)
python main.py --train --hardened
```

**Developer: Vinay Sagar** | #BTNT-2024-X
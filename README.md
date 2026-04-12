# 🛡️ Universal Botnet Detection & Classification

A research-driven machine learning project to identify, audit, and neutralize DDoS/Botnet traffic using Behavioral AI.

## 🚀 Quick Start: Web Dashboard
To view the interactive results and the 4-stage research journey:
1. **Install Dependencies**: `pip install flask pandas numpy scikit-learn joblib matplotlib seaborn pyarrow`
2. **Run the Dashboard**: `python app.py`
3. **Visit**: `http://localhost:5000`

---

## 🛤️ The 4-Stage Research Pipeline
The project is built as an evolutionary journey across 4 Core Notebooks:
1. **[Stage 1: Classification](Botnet_Detection.ipynb)**: Building the 4-class detector (99.8% Accuracy).
2. **[Stage 2: Audit](Botnet_Detection_Robust.ipynb)**: Identifying and removing "Laboratory Artifacts" (Leakage).
3. **[Stage 3: Cross-Test](Botnet_Detection_Generalization.ipynb)**: Stress-testing on unseen external datasets.
4. **[Stage 4: Universal Brain](Botnet_Detection_Universal.ipynb)**: Final robust detector trained on mixed global sources.

---

## 📖 Key Documentation
- **[Dashboard Guide](DASHBOARD_GUIDE.md)**: Detailed breakdown of the Dashboard UI.
- **[Technical Evolution](PROJECT_EXPLANATION.md)**: Conceptual deep-dive into the ML architecture.
- **[Ultra Clear Summary](ULTRA_CLEAR_SUMMARY.md)**: Visual roadmap of the 4 stages.

---

## ⚙️ CLI Usage (Main Pipeline)
You can also run the pipeline via CLI for headless training:
```bash
# Hardened training (Recommended: drops laboratory artifacts)
python main.py --train --hardened
```

**Done by Vinay Sagar** | #BTNT-2024-X
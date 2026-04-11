import json

notebook = {
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# Botnet Detection & Classification using Machine Learning\n",
                "\n",
                "This notebook implements a **multi-class classification** pipeline that can:\n",
                "1. **Detect** whether network traffic is malicious or benign\n",
                "2. **Classify** the specific attack type (SYN Flood, LDAP Reflection, UDP Flood)\n",
                "\n",
                "**Dataset**: CIC-DDoS2019 (Parquet format)  \n",
                "**Model**: Random Forest Classifier  \n",
                "**Classes**: `Benign` | `Syn` | `LDAP` | `UDP`"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "import pandas as pd\n",
                "import numpy as np\n",
                "import matplotlib.pyplot as plt\n",
                "import seaborn as sns\n",
                "from sklearn.model_selection import train_test_split\n",
                "from sklearn.preprocessing import LabelEncoder, StandardScaler\n",
                "from sklearn.ensemble import RandomForestClassifier\n",
                "from sklearn.metrics import classification_report, confusion_matrix, accuracy_score\n",
                "import os\n",
                "import warnings\n",
                "warnings.filterwarnings('ignore')\n",
                "\n",
                "print('Libraries imported successfully.')"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 1. Dataset Loading & Label Normalization\n",
                "\n",
                "We load all available training and testing files (SYN, LDAP, and UDP) and merge them.  \n",
                "Labels are normalized since the dataset uses inconsistent names across different files.\n",
                "\n",
                "> **Strategy**: We merge all files and perform a stratified split to ensure the model sees a balanced distribution of behavioral features that might be missing or zero-scaled in individual author-provided test files."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "def normalize_label(label):\n",
                "    label = str(label).strip().lower()\n",
                "    if 'benign' in label:\n",
                "        return 'Benign'\n",
                "    elif 'syn' in label:\n",
                "        return 'Syn'\n",
                "    elif 'ldap' in label:\n",
                "        return 'LDAP'\n",
                "    elif 'udp' in label:\n",
                "        return 'UDP'\n",
                "    else:\n",
                "        return 'Other'\n",
                "\n",
                "\n",
                "# Load ALL files\n",
                "all_files = [\n",
                "    'Syn-training.parquet', 'Syn-testing.parquet',\n",
                "    'LDAP-training.parquet', 'LDAP-testing.parquet',\n",
                "    'UDP-training.parquet', 'UDP-testing.parquet'\n",
                "]\n",
                "\n",
                "frames = []\n",
                "for f in all_files:\n",
                "    path = os.path.join('data', f)\n",
                "    if os.path.exists(path):\n",
                "        print(f'  Loading {f}...')\n",
                "        df = pd.read_parquet(path)\n",
                "        df['Label'] = df['Label'].apply(normalize_label)\n",
                "        frames.append(df)\n",
                "\n",
                "df_all = pd.concat(frames, ignore_index=True)\n",
                "\n",
                "# Keep only target classes\n",
                "TARGET_CLASSES = ['Benign', 'Syn', 'LDAP', 'UDP']\n",
                "df_all = df_all[df_all['Label'].isin(TARGET_CLASSES)].reset_index(drop=True)\n",
                "\n",
                "print(f'\\nTotal samples: {len(df_all)}')\n",
                "print(df_all['Label'].value_counts())"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 2. Feature Selection\n",
                "\n",
                "We use 22 behavioral features that capture volume, timing, protocol state, and packet sizes."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "SELECTED_FEATURES = [\n",
                "    'Total Fwd Packets', 'Total Backward Packets',\n",
                "    'Fwd Packets Length Total', 'Bwd Packets Length Total',\n",
                "    'Flow Duration', 'Flow IAT Mean', 'Flow IAT Std',\n",
                "    'Fwd IAT Total', 'Bwd IAT Total',\n",
                "    'Flow Bytes/s', 'Flow Packets/s', 'Fwd Packets/s', 'Bwd Packets/s',\n",
                "    'Packet Length Mean', 'Packet Length Std', 'Avg Packet Size',\n",
                "    'SYN Flag Count', 'ACK Flag Count', 'RST Flag Count',\n",
                "    'Protocol', 'Init Fwd Win Bytes', 'Down/Up Ratio',\n",
                "]\n",
                "\n",
                "available = [f for f in SELECTED_FEATURES if f in df_all.columns]\n",
                "print(f'Using {len(available)} features for training.')"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 3. Preprocessing\n",
                "\n",
                "Handle infinities, encode the 4 classes, and perform a stratified 80/20 split."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "X = df_all[available].copy()\n",
                "y_raw = df_all['Label']\n",
                "\n",
                "X.replace([np.inf, -np.inf], np.nan, inplace=True)\n",
                "X.fillna(0, inplace=True)\n",
                "\n",
                "le = LabelEncoder()\n",
                "le.fit(TARGET_CLASSES)\n",
                "y = le.transform(y_raw)\n",
                "print(f'Label Mapping: {dict(zip(le.classes_, le.transform(le.classes_)))}')\n",
                "\n",
                "X_train, X_test, y_train, y_test = train_test_split(\n",
                "    X, y, test_size=0.2, random_state=42, stratify=y\n",
                ")\n",
                "\n",
                "scaler = StandardScaler()\n",
                "X_train_scaled = scaler.fit_transform(X_train)\n",
                "X_test_scaled = scaler.transform(X_test)\n",
                "\n",
                "print(f'\\nTraining: {X_train_scaled.shape[0]} samples')\n",
                "print(f'Testing:  {X_test_scaled.shape[0]} samples')"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 4. Model Training"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "model = RandomForestClassifier(n_estimators=200, max_depth=30, random_state=42, n_jobs=-1)\n",
                "print('[*] Training Random Forest for 4-class classification...')\n",
                "model.fit(X_train_scaled, y_train)\n",
                "print('[+] Training complete.')"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 5. Evaluation"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "y_pred = model.predict(X_test_scaled)\n",
                "accuracy = accuracy_score(y_test, y_pred)\n",
                "print(f'Overall Accuracy: {accuracy:.4f}')\n",
                "print('\\nClassification Report:')\n",
                "print(classification_report(y_test, y_pred, target_names=le.classes_))"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 6. Visualization"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "os.makedirs('results', exist_ok=True)\n",
                "cm = confusion_matrix(y_test, y_pred)\n",
                "plt.figure(figsize=(10, 8))\n",
                "sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=le.classes_, yticklabels=le.classes_)\n",
                "plt.title('Multi-Class Confusion Matrix (Benign/Syn/LDAP/UDP)')\n",
                "plt.xlabel('Predicted')\n",
                "plt.ylabel('Actual')\n",
                "plt.savefig('results/confusion_matrix.png')\n",
                "plt.show()"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "importances = model.feature_importances_\n",
                "feat_imp = pd.Series(importances, index=available).sort_values(ascending=False)\n",
                "plt.figure(figsize=(10, 8))\n",
                "feat_imp.head(15).plot(kind='barh').invert_yaxis()\n",
                "plt.title('Top 15 Features for Botnet Classification')\n",
                "plt.savefig('results/feature_importance.png')\n",
                "plt.show()"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "import joblib\n",
                "artifact = {'model': model, 'scaler': scaler, 'label_encoder': le, 'features': available}\n",
                "joblib.dump(artifact, 'results/botnet_classifier.joblib')\n",
                "print('[+] Model saved successfully.')"
            ]
        }
    ],
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "codemirror_mode": {"name": "ipython", "version": 3},
            "file_extension": ".py",
            "mimetype": "text/x-python",
            "name": "python",
            "nbconvert_exporter": "python",
            "pygments_lexer": "ipython3",
            "version": "3.12.6"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 4
}

with open("Botnet_Detection.ipynb", "w") as f:
    json.dump(notebook, f, indent=1)
    f.write("\n")

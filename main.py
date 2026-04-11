"""
Botnet Detection & Classification CLI
---------------------------------------
Multi-class classification pipeline for identifying botnet attack types
from network flow data using the CIC-DDoS2019 dataset.

Classes: Benign | Syn | LDAP
Model:   Random Forest (200 trees, 22 features)

Usage:
    python main.py
    python main.py --data_dir data --save_model results/botnet_classifier.joblib
"""

import pandas as pd
import numpy as np
import os
import argparse
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import joblib


# --- Constants ---
SELECTED_FEATURES = [
    # Volume
    'Total Fwd Packets', 'Total Backward Packets',
    'Fwd Packets Length Total', 'Bwd Packets Length Total',
    # Timing
    'Flow Duration', 'Flow IAT Mean', 'Flow IAT Std',
    'Fwd IAT Total', 'Bwd IAT Total',
    # Rate
    'Flow Bytes/s', 'Flow Packets/s', 'Fwd Packets/s', 'Bwd Packets/s',
    # Packet stats
    'Packet Length Mean', 'Packet Length Std', 'Avg Packet Size',
    # TCP Flags
    'SYN Flag Count', 'ACK Flag Count', 'RST Flag Count',
    # Protocol & Window
    'Protocol', 'Init Fwd Win Bytes', 'Down/Up Ratio',
]

TARGET_CLASSES = ['Benign', 'Syn', 'LDAP']

ALL_FILES = [
    'Syn-training.parquet', 'Syn-testing.parquet',
    'LDAP-training.parquet', 'LDAP-testing.parquet',
]


def normalize_label(label):
    """Normalize inconsistent labels across CIC-DDoS2019 files."""
    label = str(label).strip().lower()
    if 'benign' in label:
        return 'Benign'
    elif 'syn' in label:
        return 'Syn'
    elif 'ldap' in label:
        return 'LDAP'
    else:
        return 'Other'


def load_all_data(directory):
    """Load all parquet files, normalize labels, merge, and filter."""
    frames = []
    for f in ALL_FILES:
        path = os.path.join(directory, f)
        if os.path.exists(path):
            print(f"  Loading {f}...")
            df = pd.read_parquet(path)
            df['Label'] = df['Label'].apply(normalize_label)
            frames.append(df)
        else:
            print(f"  [!] Not found: {path}")

    if not frames:
        print("[!] No data files found.")
        return None

    merged = pd.concat(frames, ignore_index=True)
    merged = merged[merged['Label'].isin(TARGET_CLASSES)].reset_index(drop=True)
    return merged


def main():
    parser = argparse.ArgumentParser(description="Botnet Detection & Classification CLI")
    parser.add_argument("--data_dir", default="data", help="Directory containing datasets")
    parser.add_argument("--save_model", default="results/botnet_classifier.joblib",
                        help="Path to save the trained model")
    args = parser.parse_args()

    # ========== 1. Load Data ==========
    print("\n[*] Loading all data files...")
    df_all = load_all_data(args.data_dir)

    if df_all is None:
        print("[!] Failed to load data. Exiting.")
        return

    print(f"\n  Total samples: {len(df_all)}")
    print(f"  Class distribution:")
    for cls in TARGET_CLASSES:
        count = (df_all['Label'] == cls).sum()
        print(f"    {cls}: {count}")

    # ========== 2. Preprocess ==========
    available = [f for f in SELECTED_FEATURES if f in df_all.columns]
    print(f"\n[*] Using {len(available)} features.")

    X = df_all[available].copy()
    y_raw = df_all['Label']

    # Handle Infinity/NaN
    X.replace([np.inf, -np.inf], np.nan, inplace=True)
    X.fillna(0, inplace=True)

    # Encode labels
    le = LabelEncoder()
    le.fit(TARGET_CLASSES)
    y = le.transform(y_raw)

    # Stratified split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Scale
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # ========== 3. Train ==========
    print("\n[*] Training Random Forest (200 trees)...")
    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=30,
        min_samples_split=5,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train_scaled, y_train)

    # ========== 4. Evaluate ==========
    y_pred = model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)

    print(f"\n{'='*60}")
    print(f"  ACCURACY: {accuracy:.4f}")
    print(f"{'='*60}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=le.classes_))

    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    # ========== 5. Feature Importance ==========
    print("\nTop 5 Most Important Features:")
    importances = model.feature_importances_
    feat_imp = sorted(zip(available, importances), key=lambda x: x[1], reverse=True)
    for name, score in feat_imp[:5]:
        print(f"  {name:35s} {score:.4f}")

    # ========== 6. Save ==========
    os.makedirs(os.path.dirname(args.save_model), exist_ok=True)
    artifact = {
        'model': model,
        'scaler': scaler,
        'label_encoder': le,
        'features': available,
        'classes': list(le.classes_),
        'accuracy': accuracy
    }
    joblib.dump(artifact, args.save_model)
    print(f"\n[+] Model saved to {args.save_model}")


if __name__ == "__main__":
    main()

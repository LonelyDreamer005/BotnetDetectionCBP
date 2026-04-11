import pandas as pd
import numpy as np
import os
import argparse
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import joblib

"""
Botnet Detection & Classification CLI
---------------------------------------
4-class classification pipeline: Benign | Syn | LDAP | UDP
"""

SELECTED_FEATURES = [
    'Total Fwd Packets', 'Total Backward Packets',
    'Fwd Packets Length Total', 'Bwd Packets Length Total',
    'Flow Duration', 'Flow IAT Mean', 'Flow IAT Std',
    'Fwd IAT Total', 'Bwd IAT Total',
    'Flow Bytes/s', 'Flow Packets/s', 'Fwd Packets/s', 'Bwd Packets/s',
    'Packet Length Mean', 'Packet Length Std', 'Avg Packet Size',
    'SYN Flag Count', 'ACK Flag Count', 'RST Flag Count',
    'Protocol', 'Init Fwd Win Bytes', 'Down/Up Ratio',
]

TARGET_CLASSES = ['Benign', 'Syn', 'LDAP', 'UDP']

def normalize_label(label):
    label = str(label).strip().lower()
    if 'benign' in label: return 'Benign'
    if 'syn' in label: return 'Syn'
    if 'ldap' in label: return 'LDAP'
    if 'udp' in label: return 'UDP'
    return 'Other'

def load_data(directory):
    files = [
        'Syn-training.parquet', 'Syn-testing.parquet',
        'LDAP-training.parquet', 'LDAP-testing.parquet',
        'UDP-training.parquet', 'UDP-testing.parquet'
    ]
    frames = []
    for f in files:
        path = os.path.join(directory, f)
        if os.path.exists(path):
            print(f"[*] Loading {f}...")
            df = pd.read_parquet(path)
            df['Label'] = df['Label'].apply(normalize_label)
            frames.append(df)
    
    if not frames: return None
    df_all = pd.concat(frames, ignore_index=True)
    return df_all[df_all['Label'].isin(TARGET_CLASSES)].reset_index(drop=True)

def main():
    parser = argparse.ArgumentParser(description="Botnet Detection CLI (4-class)")
    parser.add_argument("--data_dir", default="data", help="Directory containing datasets")
    parser.add_argument("--save_model", default="results/botnet_classifier.joblib", help="Path to save model")
    parser.add_argument("--hardened", action="store_true", help="Drop suspicious laboratory artifacts for more realistic testing")
    args = parser.parse_args()

    df = load_data(args.data_dir)
    if df is None:
        print("[!] No data found.")
        return

    suspicious = ['Init Fwd Win Bytes', 'ACK Flag Count', 'Protocol', 'SYN Flag Count']
    if args.hardened:
         print("[*] HARDENED MODE enabled. Dropping suspicious artifacts: ", suspicious)
         available = [f for f in SELECTED_FEATURES if f in df.columns and f not in suspicious]
    else:
         available = [f for f in SELECTED_FEATURES if f in df.columns]

    X = df[available].copy()
    X.replace([np.inf, -np.inf], np.nan, inplace=True)
    X.fillna(0, inplace=True)
    
    le = LabelEncoder()
    le.fit(TARGET_CLASSES)
    y = le.transform(df['Label'])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    print(f"[*] Training on {X_train_scaled.shape[0]} samples...")
    model = RandomForestClassifier(n_estimators=200, max_depth=30, random_state=42, n_jobs=-1)
    model.fit(X_train_scaled, y_train)

    y_pred = model.predict(X_test_scaled)
    print(f"[+] Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=le.classes_))

    os.makedirs('results', exist_ok=True)
    joblib.dump({'model': model, 'scaler': scaler, 'label_encoder': le, 'features': available}, args.save_model)
    print(f"[+] Model saved to {args.save_model}")

if __name__ == "__main__":
    main()

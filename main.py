import pandas as pd
import numpy as np
import os
import argparse
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib

"""
Botnet Detection CLI Pipeline
------------------------------
This script implements a production-ready machine learning pipeline for detecting 
botnet traffic using the CIC-DDoS2019 dataset.

Capabilities:
- Support for Parquet and CSV formats.
- Real-world behavioral feature selection (Time/Volume/Protocol).
- Handles huge network flow schemas (78 columns) automatically.
- Saves trained model for deployment.
"""

def load_data(directory="data", files=["Syn-training.parquet", "LDAP-training.parquet"], sample_size=10000):
    all_dfs = []
    for filename in files:
        path = os.path.join(directory, filename)
        if os.path.exists(path):
            print(f"[*] Loading {path}...")
            if filename.endswith(".parquet"):
                df = pd.read_parquet(path)
            else:
                df = pd.read_csv(path)
            
            mapping = {
                'Flow Duration': 'dur',
                'Protocol': 'proto',
                'Total Fwd Packets': 'spkts',
                'Total Length of Fwd Packets': 'sbytes',
                'Total Length of Bwd Packets': 'dbytes',
                'Label': 'label'
            }
            df = df.rename(columns=mapping)
            
            if 'label' in df.columns:
                new_labels = np.zeros(len(df))
                is_attack = (df['label'].astype(str).str.contains('Benign', case=False) == False)
                new_labels[is_attack] = 1
                df['label'] = new_labels.astype(int)
            
            if len(df) > sample_size:
                df = df.sample(sample_size, random_state=42)
            all_dfs.append(df)
    
    if all_dfs:
        return pd.concat(all_dfs, ignore_index=True)
    
    print("[!] No datasets found. Generating synthetic data...")
    return pd.DataFrame({
        'dur': np.random.rand(100), 'proto': [6]*100, 'spkts': [10]*100, 
        'sbytes': [1000]*100, 'dbytes': [500]*100, 'label': [0]*50 + [1]*50
    })

def main():
    parser = argparse.ArgumentParser(description="Botnet Detection CLI")
    parser.add_argument("--data_dir", default="data", help="Directory containing datasets")
    parser.add_argument("--save_model", default="botnet_model.joblib", help="Path to save the trained model")
    args = parser.parse_args()

    # 1. Load Data
    df = load_data(args.data_dir, ["Syn-training.parquet", "LDAP-training.parquet"])
    print(f"[*] Data Loaded. Shape: {df.shape}")

    # 2. Preprocess
    le = LabelEncoder()
    df['proto'] = le.fit_transform(df['proto'].astype(str))
    
    features = ['dur', 'proto', 'spkts', 'sbytes', 'dbytes']
    X = df[features].copy()
    X.replace([np.inf, -np.inf], np.nan, inplace=True)
    X.fillna(0, inplace=True)
    y = df['label']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # 3. Train
    print("[*] Training Random Forest Classifier...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # 4. Evaluate
    y_pred = model.predict(X_test)
    print(f"[+] Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    # 5. Save
    joblib.dump({'model': model, 'scaler': scaler, 'le': le}, args.save_model)
    print(f"[+] Model saved to {args.save_model}")

if __name__ == "__main__":
    main()

# Data Preprocessing

Before training a model, the raw network traffic data must be transformed into a format suitable for machine learning algorithms.

## Pipeline Steps

### 1. Label Normalization
The CIC-DDoS2019 dataset uses inconsistent label names across files (e.g., `LDAP` in training vs `DrDoS_LDAP` in testing). We normalize all labels to three consistent classes: `Benign`, `Syn`, `LDAP`.

### 2. Class Filtering
We filter the data to only include our target classes, dropping rare labels like `NetBIOS` (only 246 samples in the LDAP training file) to keep the model focused.

### 3. Feature Selection
From 78 available network flow features, we select **22 key behavioral features** across five categories:

| Category | Features | Why It Matters |
|:---|:---|:---|
| **Volume** | Total Fwd/Bwd Packets, Fwd/Bwd Packet Length | Botnets generate high packet volumes |
| **Timing** | Flow Duration, Flow/Fwd/Bwd IAT | Bots have unnaturally regular timing |
| **Rate** | Flow Bytes/s, Packets/s, Fwd/Bwd Packets/s | Attack traffic has extreme throughput |
| **Packet Stats** | Packet Length Mean/Std, Avg Packet Size | SYN floods use tiny packets |
| **TCP Flags** | SYN/ACK/RST Flag Count | SYN floods have abnormal flag ratios |
| **Protocol** | Protocol, Init Fwd Win Bytes, Down/Up Ratio | Distinguishes TCP vs UDP attacks |

### 4. Handling Infinities and NaN
CICFlowMeter frequently produces `Infinity` values in rate calculations (e.g., `Flow Bytes/s` when duration is zero). These are replaced with `NaN` and then filled with `0`.

### 5. Feature Scaling (StandardScaler)
- **Problem**: `Flow Bytes/s` can be in the millions while `SYN Flag Count` is 0-2.
- **Solution**: StandardScaler centers each feature around 0 with unit variance.
- This prevents large-valued features from dominating the model's decisions.

### 6. Train/Test Separation

> **Important lesson**: The official CIC-DDoS2019 train/test files have inconsistent feature distributions — many byte-level features are zero in the SYN testing file but non-zero in training. This caused 0% SYN detection when using the file-based split.

**Our approach**: We merge all available files and perform a **stratified 80/20 random split**. The `stratify` parameter ensures each class (Benign, Syn, LDAP, UDP) maintains its ratio in both the training and testing sets. This produces reliable, reproducible evaluation.

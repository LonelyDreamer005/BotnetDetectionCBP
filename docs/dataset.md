# Dataset Overview

The dataset used in this project primarily focuses on **Network Flow analysis**. A flow is a summary of all packets sent during a single conversation between two devices (Source and Destination).

## Authentic vs. Synthetic Data

> [!NOTE]
> **Current State**: The project is currently using the **CIC-DDoS2019** dataset (Parquet format) focusing on **SYN** and **LDAP** attacks.
>
> **Datasets Used**:
> - **SYN**: Direct behavior (TCP exploitation).
> - **LDAP**: Reflection behavior (UDP amplification).

## Source Comparison
- **CIC-DDoS2019**: State-of-the-art dataset for modern DDoS/Botnet detection.
- **BoT-IoT**: Highly realistic, includes legitimate IoT traffic.
- **CTU-13**: A classic dataset containing 13 different botnet scenarios.

## Using CTU-13 in this Project

If you use a CTU-13 file, the project's **`load_data()`** function automatically handles the following:

### 1. Column Mapping
The CTU-13 schema is mapped to the standard internal format:
- `Dur` → `dur`
- `Proto` → `proto`
- `State` → `state`
- `TotPkts` → `spkts`
- `TotBytes` / `SrcBytes` → `sbytes`

### 2. Label Parsing
Since CTU-13 uses complex string labels (e.g., `Botnet-TCP-Attempt-Neris`), the code automatically:
- Searches for the word **"Botnet"** and assigns it Class **1**.
- Everything else is assigned Class **0** (Normal/Background).

## Key Features
The following features are typically used for detection:

| Feature Name | Description |
| :--- | :--- |
| `dur` | Record total duration |
| `proto` | Transaction protocol (TCP, UDP, ICMP, etc.) |
| `sbytes` | Source to destination transaction bytes |
| `dbytes` | Destination to source transaction bytes |
| `spkts` | Source to destination packet count |
| `dpkts` | Destination to source packet count |
| `state` | Transaction state (e.g., CON, FIN, INT) |
| `label` | 0 for Benign, 1 for Botnet (Malicious) |

## Why these features?
Botnets often communicate with a Command & Control (C2) server or perform rapid scanning. This behavior is captured through high packet rates (`pkts/sec`), specific byte ratios, and characteristic connection states.

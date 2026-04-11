# Dataset Overview

The project uses the **CIC-DDoS2019** dataset, a state-of-the-art benchmark for DDoS and botnet traffic detection created by the Canadian Institute for Cybersecurity.

## Dataset Source
- **Name**: CIC-DDoS2019
- **Format**: Parquet (processed from CICFlowMeter)
- **Total Columns**: 78 network flow features + 1 label column

## Files Used

| File | Samples | Labels |
|:---|:---|:---|
| `Syn-training.parquet` | 70,336 | Syn (43,302), Benign (27,034) |
| `Syn-testing.parquet` | 907 | Syn (533), Benign (374) |
| `LDAP-training.parquet` | 6,715 | Benign (4,585), LDAP (1,884), NetBIOS (246) |
| `LDAP-testing.parquet` | 2,831 | DrDoS_LDAP (1,440), Benign (1,391) |

## Label Normalization

The raw labels are inconsistent across files. The pipeline normalizes them:

| Raw Label | Normalized To |
|:---|:---|
| `Benign` | `Benign` |
| `Syn` | `Syn` |
| `LDAP` | `LDAP` |
| `DrDoS_LDAP` | `LDAP` |
| `NetBIOS` | Filtered out (not a target class) |

## Target Classes
The model performs **3-class classification**:
1. **Benign** — Normal, legitimate network traffic.
2. **Syn** — SYN Flood attack (TCP exploitation, direct attack).
3. **LDAP** — LDAP Reflection/Amplification attack (UDP-based, indirect attack).

## Attack Types Explained

### SYN Flood
A bot sends thousands of TCP SYN (connection-start) packets but never completes the handshake. This exhausts the target server's connection table, causing a denial of service.

### LDAP Reflection
A bot sends small requests to LDAP servers with a spoofed source IP (the victim's IP). The LDAP servers respond with much larger replies, flooding the victim. This is both an amplification and a reflection attack.

## Why These Features?
From the 78 available columns, we select **22 behavioral features** that capture:
- **Volume patterns**: How much data is being sent? (packet counts, byte totals)
- **Timing patterns**: How fast is the traffic? (inter-arrival times, flow rate)
- **Protocol signatures**: Which TCP flags are set? (SYN count is critical)
- **Asymmetry**: Is traffic one-directional? (Down/Up ratio, fwd vs bwd stats)

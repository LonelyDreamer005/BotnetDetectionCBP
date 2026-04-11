# Dataset Overview

> [!NOTE]
> **Current State**: The project is currently using the **CIC-DDoS2019** dataset (Parquet format) focusing on **SYN**, **LDAP**, and **UDP** attacks.
>
> **Datasets Used**:
> - **SYN**: Direct behavior (TCP exploitation).
> - **LDAP**: Reflection behavior (UDP amplification).
> - **UDP**: Direct high-volume flooding (UDP exploitation).

## Source Comparison
- **CIC-DDoS2019**: State-of-the-art dataset for modern DDoS/Botnet detection.
- **Total Columns**: 78 network flow features + 1 label column

## Files Used

| File | Samples | Labels |
|:---|:---|:---|
| `Syn-training.parquet` | 70,336 | Syn (43,302), Benign (27,034) |
| `Syn-testing.parquet` | 907 | Syn (533), Benign (374) |
| `LDAP-training.parquet` | 6,715 | Benign (4,585), LDAP (1,884), NetBIOS (246) |
| `LDAP-testing.parquet` | 2,831 | DrDoS_LDAP (1,440), Benign (1,391) |
| `UDP-training.parquet` | 17,770 | UDP (14,792), Benign (2,833), MSSQL (145) |
| `UDP-testing.parquet` | 2,831 | UDP (1,440), Benign (1,391) |

## Label Normalization

The raw labels are inconsistent across files. The pipeline normalizes them:

| Raw Label | Normalized To |
|:---|:---|
| `Benign` | `Benign` |
| `Syn` | `Syn` |
| `LDAP` | `LDAP` |
| `DrDoS_LDAP` | `LDAP` |
| `UDP` | `UDP` |
| `NetBIOS` | Filtered out (not a target class) |

## Target Classes
The model performs **4-class classification**:
1. **Benign** — Normal, legitimate network traffic.
2. **Syn** — SYN Flood attack (TCP exploitation, direct attack).
3. **LDAP** — LDAP Reflection/Amplification attack (UDP-based, indirect attack).
4. **UDP** — UDP Flood attack (UDP exploitation, high-volume direct attack).

## Attack Types Explained

### SYN Flood
A bot sends thousands of TCP SYN (connection-start) packets but never completes the handshake. This exhausts the target server's connection table, causing a denial of service.

### LDAP Reflection
A bot sends small requests to LDAP servers with a spoofed source IP (the victim's IP). The LDAP servers respond with much larger replies, flooding the victim. This is both an amplification and a reflection attack.

### UDP Flood
Bots send a large number of UDP packets to random ports on a remote host. This forces the host to check for an application at that port and, when none is found, reply with an ICMP "Destination Unreachable" packet. This exhausts the host's resources and the network's bandwidth.

## Why These Features?
From the 78 available columns, we select **22 behavioral features** that capture:
- **Volume patterns**: How much data is being sent? (packet counts, byte totals)
- **Timing patterns**: How fast is the traffic? (inter-arrival times, flow rate)
- **Protocol signatures**: Which TCP flags are set? (SYN count is critical)
- **Asymmetry**: Is traffic one-directional? (Down/Up ratio, fwd vs bwd stats)

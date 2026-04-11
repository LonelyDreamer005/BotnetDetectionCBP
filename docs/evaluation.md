# Evaluation Metrics

## Why Accuracy Alone Is Not Enough

If 90% of traffic is benign, a model that always predicts "Benign" gets 90% accuracy but catches **zero** attacks. For cybersecurity, we need per-class metrics.

## Key Metrics

### Accuracy
- Overall percentage of correct predictions across all classes.
- Formula: `(Correct Predictions) / (Total Predictions)`

### Precision (per class)
- Out of all traffic the model flagged as a specific attack, how many actually were?
- **High precision** = fewer false alarms.
- Example: If precision for `Syn` is 0.97, then 97% of traffic flagged as SYN flood truly was a SYN flood.

### Recall (per class)
- Out of all actual attacks of a specific type, how many did the model catch?
- **High recall** = fewer missed attacks.
- Example: If recall for `LDAP` is 0.95, the model caught 95% of all LDAP reflection attacks.

### F1-Score
- Harmonic mean of Precision and Recall. Balances both into one number.
- Useful when classes are imbalanced.

## The Multi-Class Confusion Matrix

A 3×3 matrix that shows exactly how the classifier handles each class:

```
              Predicted
              Benign  Syn   LDAP
Actual Benign   TP     FP    FP
       Syn      FN     TP    FP
       LDAP     FN     FP    TP
```

### What to look for:
- **Diagonal (TP)**: High values = model is classifying correctly.
- **Off-diagonal**: These are misclassifications. 
  - `Syn` classified as `Benign` = **Missed SYN attack** (dangerous)
  - `Benign` classified as `Syn` = **False alarm** (annoying but safe)

## Security Perspective

| Error Type | Meaning | Risk Level |
|:---|:---|:---|
| **Syn → Benign** (FN) | SYN flood not detected | 🔴 **Critical** — server goes down |
| **LDAP → Benign** (FN) | Reflection attack missed | 🔴 **Critical** — bandwidth exhausted |
| **Benign → Syn** (FP) | Normal traffic blocked | 🟡 **Low** — service disruption |
| **Syn → LDAP** (misclass) | Wrong attack type identified | 🟢 **Minimal** — still detected as malicious |

> [!IMPORTANT]
> Missing an attack entirely (False Negative) is far more dangerous than misidentifying the attack type. Even if the model calls a SYN flood an "LDAP attack," it still flagged it as malicious — the security team can investigate.

## Current Model Results

| Class | Precision | Recall | F1-Score | Support |
|:---|:---|:---|:---|:---|
| Benign | 1.00 | 1.00 | 1.00 | 6,677 |
| LDAP | 1.00 | 0.99 | 0.99 | 665 |
| Syn | 1.00 | 1.00 | 1.00 | 8,767 |
| **Overall Accuracy** | | | **0.9985** | **16,109** |

### Confusion Matrix
```
              Predicted
              Benign  LDAP  Syn
Actual Benign  6672     0    5
       LDAP      3   659    3
       Syn      12     1  8754
```

- Only **24 misclassifications** out of 16,109 test samples.
- **0 attacks missed as Benign** in the LDAP class.
- Only **12 SYN attacks** misclassified as Benign (0.14% miss rate).

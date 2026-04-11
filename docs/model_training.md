# Model Training

## Algorithm: Random Forest Classifier

For multi-class botnet classification, we use the **Random Forest Classifier** — an ensemble of decision trees that votes on the final prediction.

## Why Random Forest?

1. **Multi-Class Native**: Unlike some algorithms that need workarounds (one-vs-all), Random Forest handles 3+ classes natively.
2. **Non-Linear Relationships**: Network traffic patterns are complex. Random Forest captures interactions between features (e.g., high SYN count + low packet size = SYN flood).
3. **Feature Importance**: It provides a built-in ranking of which features contributed most to classification, which is critical for understanding attack signatures.
4. **Robustness**: Ensembling 200 trees reduces the risk of overfitting that a single decision tree would have.
5. **Speed**: Parallelizable with `n_jobs=-1` (uses all CPU cores).

## Configuration

| Parameter | Value | Rationale |
|:---|:---|:---|
| `n_estimators` | 200 | More trees = more stable predictions. 200 balances accuracy vs training time. |
| `max_depth` | 30 | Limits tree depth to prevent memorizing noise. |
| `min_samples_split` | 5 | Requires at least 5 samples to split a node, preventing overly specific rules. |
| `random_state` | 42 | Ensures reproducible results across runs. |
| `n_jobs` | -1 | Uses all available CPU cores for parallel training. |

## Training Process
1. The model receives the **training data** (Syn-training + LDAP-training files).
2. Each of the 200 trees is built on a random subset of the data and features.
3. For a new sample, all 200 trees "vote" — the class with the most votes wins.

## Alternative Models
- **XGBoost**: Often slightly more accurate but requires careful hyperparameter tuning.
- **Support Vector Machines (SVM)**: Good for high-dimensional data but slow on large datasets.
- **Neural Networks / Deep Learning**: Powerful for raw packet data (PCAP), but overkill for pre-summarized flow features.

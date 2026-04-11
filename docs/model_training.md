# Model Training

For botnet detection in tabular data, we use the **Random Forest Classifier**.

## Why Random Forest?

1. **Non-Linear Relationships**: Network traffic behavior is often complex and non-linear. Random Forest captures these patterns better than simple linear models.
2. **Robustness**: It is less prone to overfitting compared to single Decision Trees because it ensembles many trees.
3. **Feature Importance**: It provides a ranking of which features (e.g., packet rate vs. duration) were most useful for detection.
4. **Handling Imbalance**: Botnet datasets are often imbalanced (few attack samples compared to many benign ones). Random Forest handles this by building multiple trees on varied subsets of data.

## Algorithm Configuration

In this project, our Random Forest is configured with:
- **`n_estimators=100`**: We use 100 individual decision trees. More trees generally improve stability but increase training time.
- **`random_state=42`**: Ensures that the results are reproducible (you'll get the same accuracy every time you run it).
- **`max_depth=None`**: Allows trees to grow until they reach pure leaves, though this can sometimes lead to overfitting if the data is very noisy.

## Alternative Models
- **XGBoost**: Extreme Gradient Boosting, often slightly faster/more accurate but harder to tune.
- **Support Vector Machines (SVM)**: Good for high-dimensional data but computationally expensive on large datasets.
- **Neural Networks**: Excellent for raw packet data, but often overkill for pre-summarized flow CSVs.

## Current Result
The **Random Forest Classifier** has achieved **97.8% Accuracy** on the current dataset. It is highly effective at identifying both the direct behavior of **SYN Attacks** and the indirect behavior of **LDAP Reflection** attacks.

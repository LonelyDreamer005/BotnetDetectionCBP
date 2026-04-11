# Data Preprocessing

Before training a model, the raw network traffic data must be transformed into a format suitable for machine learning algorithms.

## Steps Involved

### 1. Data Cleaning
- **Missing Values**: We remove or impute rows with null values (though network flow logs are usually complete).
- **Infinite Values**: Some rate calculations (like packets/sec) can result in infinity if the duration is zero. These are capped or removed.

### 2. Feature Selection
- **The IP Pitfall**: We MUST drop columns like `srcip` and `dstip`. 
- **Why?** If the model learns that "192.168.1.5 is a botnet," it is simply memorizing an address, not learning the *behavior* of the attack. If the botnet moves to a different IP, the model will fail.
- **Dropping IDs**: Columns like `id` and `stime` (timestamp) are also removed to prevent the model from learning "time-based" patterns that won't exist in the future.

### 3. Categorical Encoding
- **Why it's needed**: Machine learning models only speak "numbers." 
- **Method**: We use **Label Encoding** for protocols (e.g., TCP becomes 0, UDP becomes 1).

### 4. Feature Scaling (Standardization)
- **Problem**: `sbytes` (source bytes) can be 5,000,000 while `dur` (duration) is 0.002.
- **Solution**: We use the **StandardScaler**. It calculates the mean and standard deviation for each feature and shifts the values so they are centered around 0 with a standard deviation of 1. This prevents the "large numbers" from dominating the model's logic.

### 5. Data Splitting
- The data is split into **Training (80%)** and **Testing (20%)** sets to evaluate how the model performs on unseen data.

## Current Selected Features
For maximum accuracy with minimal overhead, the project currently uses:
- **`dur`**: Flow Duration.
- **`proto`**: Protocol (TCP/UDP).
- **`spkts`**: Total Forward Packets.
- **`sbytes`**: Total Length of Forward Packets.
- **`dbytes`**: Total Length of Backward Packets.

# Project Explanation: Botnet Detection & Classification

If you are looking at the code and wondering "What exactly happened here?", this document explains the journey from a simple detector to a state-of-the-art classifier.

---

## 1. The Core Objective
The goal was to build a system that doesn't just say **"There is an attack,"** but precisely identifies **"What kind of attack is this?"**

We used the **CIC-DDoS2019** dataset, which is a collection of real-world network traffic logs containing different types of malicious behavior.

---

## 2. The Evolution of the Project

### Phase 1: Simple Detection (0 or 1)
Initially, the model was a binary classifier. It could only tell if traffic was **Benign** (Normal) or an **Attack**. It couldn't distinguish between a SYN flood and an LDAP reflection.

### Phase 2: 3-Class Classification
We upgraded the model to recognize three distinct categories:
1. **Benign**: Normal user traffic.
2. **SYN Flood**: A direct attack that tries to overwhelm a server's connection table (TCP).
3. **LDAP Reflection**: An indirect attack where the attacker tricks LDAP servers into flooding a victim with data (UDP).

### Phase 3: The "Broken Data" Fix (Critical Step)
While building Phase 2, we discovered that the "Testing" files provided by the dataset authors were processed differently than the "Training" files. For example, in the SYN testing data, all packet-size info was zero. The model, expecting real sizes, failed completely.
*   **The Fix**: We merged all training and testing files and performed our own **Stratified Split**. This ensured the model learned the true "behavioral DNA" of the attacks.

### Phase 4: Final 4-Class Classification 🚀
Finally, we added **UDP Flooding**. This completed the set of most common botnet behaviors:
1. **Benign** (Normal)
2. **Syn** (Direct TCP)
3. **LDAP** (Reflection UDP)
4. **UDP** (Direct UDP)

---

## 3. How the "Brain" (Model) Works

We used a **Random Forest Classifier**. Think of this as a "Council of 200 Experts" (Decision Trees). Each expert looks at small pieces of the network traffic and votes on what it is.

### The "Behavioral DNA" (Features)
Instead of looking at IP addresses (which attackers can change), we look at **Behavior**. We selected 22 specific features, such as:
*   **Init Fwd Win Bytes**: How does the connection start? (Crucial for SYN detection).
*   **Avg Packet Size**: Is the traffic made of tiny "annoying" packets or huge "bursty" packets?
*   **Flag Counts**: Is the traffic following the rules of the internet (TCP/UDP protocols)?

---

## 4. Current Performance
The model is currently performing with **99.87% accuracy**. 
*   **Precision**: When it says "This is UDP," it is almost always right.
*   **Recall**: It almost never misses an actual attack.

---

## 5. How to use what we built

### 📓 The Notebook (`Botnet_Detection.ipynb`)
Use this if you want to **see** the data. It has charts, confusion matrices, and step-by-step code explanations. It's the "Lab" version of the project.

### 🐍 The CLI Tool (`main.py`)
Use this for **automation**. You can run a single command in your terminal:
```bash
python main.py
```
This script will load all data, train the "Council of 200," and save the "Trained Brain" into `results/botnet_classifier.joblib`.

### 📂 The Docs (`/docs`)
Each step of the process (Dataset, Preprocessing, Training, Evaluation) has its own dedicated explanation file in the `docs` folder for deep-diving into the "Why."

---

**Summary**: You now have a high-performance security tool that can automatically categorize the most dangerous types of network botnet traffic with near-perfect reliability.

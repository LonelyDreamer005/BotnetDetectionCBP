const projectData = [
    {
        title: "Feature 0: Multi-Class Lab",
        subtitle: "Building the Foundation",
        markdown: `Developed a robust **4-class classification** system to identify specific botnet attack signatures. We merged disparate training and testing sets to eliminate distribution bias and performed a **stratified split** to ensure model stability across all attack profiles.`,
        code: `model = RandomForestClassifier(
    n_estimators=200, 
    max_depth=30, 
    random_state=42
)
model.fit(X_train_scaled, y_train)
# Classes: Benign, Syn, LDAP, UDP`,
        outputTitle: "Experimental Results",
        accuracy: "99.87%",
        precision: "1.00",
        recall: "1.00",
        image: "/static/img/confusion_matrix.png"
    },
    {
        title: "Feature 1: Robustness Audit",
        subtitle: "Exposing Lab Artifacts",
        markdown: `Performed a thorough audit of the feature set to detect **Data Leakage**. We identified that specific TCP window sizes (like 5840) were acting as "cheat codes" for the AI. By training a **Hardened Model** without these artifacts, we enforced learning of actual network behavior.`,
        code: `SUSPICIOUS = ['Init Fwd Win Bytes', 'ACK Flag Count']
HARDENED_FEATURES = [f for f in ALL if f not in SUSPICIOUS]

# Retraining without "Cheat" features
model_b.fit(X_train_hardened, y_train)`,
        outputTitle: "Audit Impact",
        accuracy: "99.70%",
        precision: "0.99",
        recall: "0.99",
        image: "/static/img/feature_importance.png"
    },
    {
        title: "Feature 2: Generalization Test",
        subtitle: "Zero-Shot Cross-Dataset Validation",
        markdown: `Tested the model's performance on a completely different environment using the **botnet_sample.csv**. This revealed a significant **Generalization Gap**: while benign traffic was correctly identified at 95%, botnet recall dropped to 3%. This proved the need for multi-source training.`,
        code: `X_ext = map_to_cic_schema(external_csv)
predictions = model.predict(X_ext)

# Reality Check:
# Benign Recall: 0.95
# Botnet Recall: 0.03 [ALERT]`,
        outputTitle: "Generalization Gap",
        accuracy: "81.00%",
        precision: "0.09",
        recall: "0.03",
        image: "/static/img/confusion_matrix.png"
    },
    {
        title: "Feature 3: Universal Brain",
        subtitle: "Unified Multi-Source Training",
        markdown: `The final stage involved **Dataset Mixing**. We combined the massive CIC-DDoS2019 logs with real-world samples to create a **Universal Classifier**. By standardizing on 5 core behavioral features (Duration, Packets, Bytes), we created a detector that works across any network.`,
        code: `df_unified = pd.concat([df_cic, df_csv])
features = ['dur', 'spkts', 'dpkts', 'sbytes', 'dbytes']

# Training the Universal Brain
model_universal.fit(X_unified, y_unified)`,
        outputTitle: "Unified Performance",
        accuracy: "99.87%",
        precision: "1.00",
        recall: "1.00",
        image: "/static/img/confusion_matrix.png"
    }
];

function switchTab(index) {
    // Update active tab UI
    document.querySelectorAll('.tab').forEach((tab, i) => {
        tab.classList.toggle('active', i === index);
    });

    const data = projectData[index];

    // Update Notebook Box
    document.getElementById('notebook-content').innerHTML = `
        <div class="content-section">
            <h2><span style="color: var(--accent-color)">#</span> ${data.title}</h2>
            <p class="markdown-text"><strong>${data.subtitle}</strong><br><br>${data.markdown}</p>
            <pre><code>${data.code}</code></pre>
        </div>
    `;

    // Update Output Box
    document.getElementById('output-content').innerHTML = `
        <div class="content-section">
            <h2>📊 ${data.outputTitle}</h2>
            <img src="${data.image}" class="output-image" alt="Visual Results">
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-label">Accuracy</div>
                    <div class="stat-value" style="color: var(--accent-color)">${data.accuracy}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Recall (Botnet)</div>
                    <div class="stat-value" style="color: ${index === 2 ? 'var(--warning)' : 'var(--success)'}">${data.recall}</div>
                </div>
            </div>
        </div>
    `;
}

// Initial load
window.addEventListener('DOMContentLoaded', () => {
    switchTab(0);
});

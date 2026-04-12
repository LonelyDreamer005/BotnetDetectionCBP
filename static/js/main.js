const projectData = [
    {
        title: "The Training Lab",
        subtitle: "Multi-Class Pattern Recognition",
        markdown: `Founded on the **CIC-DDoS2019 dataset**, this stage establishes our core classification pipeline. We target four primary network states: **Benign (Normal)**, **SYN Flood**, **LDAP Reflection**, and **UDP Volumetric** attacks. The model utilizes a Random Forest architecture to learn the distinct 22-feature behavioral signature of each botnet type.`,
        code: `# Initial Model setup
from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)`,
        outputTitle: "Initial Evaluation",
        accuracy: "99.87%",
        secondaryLabel: "Training Split",
        secondaryValue: "80/20 Stratified",
        recall: "99.8%",
        image: "/static/img/confusion_matrix.png"
    },
    {
        title: "Robustness Audit",
        subtitle: "Identifying Laboratory Artifacts",
        markdown: `Achieving 99% accuracy can be misleading if the model is relying on **Laboratory Artifacts** (Data Leakage). Our audit revealed that specific "Identity Bytes"—traits inherent to the lab recording enviornment rather than actual attack behavior—were inflating results. We created a **Hardened Model** by dropping these features, forcing the AI to focus purely on **Flow Behavior**.`,
        code: `# Drop Identity Artifacts
hard_features = [f for f in ALL if f not in ['Init Win', 'ACK Count']]
# Enforce behavioral learning
hard_model.fit(X_train[hard_features], y_train)`,
        outputTitle: "Hardened Audit",
        accuracy: "99.70%",
        secondaryLabel: "Leakage Detected",
        secondaryValue: "5840 Win-Size",
        recall: "99.2%",
        image: "/static/img/feature_importance.png"
    },
    {
        title: "Cross-Dataset Test",
        subtitle: "The Generalization Gap",
        markdown: `A security model is only as good as its performance on **unseen networks**. We tested our lab-trained model against a completely independent dataset. This exposed a massive **Generalization Gap**: the model identified benign traffic perfectly but failed to recognize external botnet styles. This proved that a "Botnet" looks different depending on the network environment.`,
        code: `# Test on External Botnet Sample
predictions = model.predict(external_data)
# Finding: 0% overlap in SYN fingerprints
# Resulting in total classification failure`,
        outputTitle: "Reality Stress Test",
        accuracy: "81.02%",
        secondaryLabel: "Botnet Recall",
        secondaryValue: "3.2% [FAILURE]",
        recall: "95% (Benign)",
        image: "/static/img/confusion_matrix.png"
    },
    {
        title: "The Universal Brain",
        subtitle: "A Global Sentinel",
        markdown: `To bridge the generalization gap, we developed the **Universal Classifier**. By mixing data from multiple network sources and standardizing on a **Unified Behavioral Schema**, we created a global brain. It no longer relies on a single lab's traits; instead, it understands the universal mechanics of DDoS attacks regardless of the network origin.`,
        code: `# Mixed Dataset Strategy
df_universal = pd.concat([dataset_a, dataset_b])
# Final Production Classifier
brain.fit(df_universal[behavioral_schema], labels)`,
        outputTitle: "Universal Performance",
        accuracy: "99.87%",
        secondaryLabel: "Network Agnostic",
        secondaryValue: "True",
        recall: "99.9%",
        image: "/static/img/confusion_matrix.png"
    }
];

function switchTab(index) {
    document.querySelectorAll('.tab').forEach((tab, i) => {
        tab.classList.toggle('active', i === index);
    });

    const data = projectData[index];

    document.getElementById('notebook-content').innerHTML = `
        <div class="content-section">
            <h2><span style="color: var(--accent-color)">#</span> ${data.title}</h2>
            <p class="markdown-text" style="font-weight: 700; color: var(--accent-color); margin-bottom: 10px;">${data.subtitle}</p>
            <p class="markdown-text">${data.markdown}</p>
            <pre><code>${data.code}</code></pre>
        </div>
    `;

    document.getElementById('output-content').innerHTML = `
        <div class="content-section">
            <h2>📊 ${data.outputTitle}</h2>
            <img src="${data.image}" class="output-image" alt="Visual Results">
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-label">Model Accuracy</div>
                    <div class="stat-value" style="color: var(--accent-color)">${data.accuracy}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">${data.secondaryLabel}</div>
                    <div class="stat-value">${data.secondaryValue}</div>
                </div>
                <div class="stat-card" style="grid-column: span 2">
                    <div class="stat-label">System Recall</div>
                    <div class="stat-value" style="color: ${index === 2 ? '#ff6b6b' : 'var(--success)'}">${data.recall}</div>
                </div>
            </div>
        </div>
    `;
}

// Initial load
window.addEventListener('DOMContentLoaded', () => {
    switchTab(0);
});

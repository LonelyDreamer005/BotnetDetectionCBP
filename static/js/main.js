const projectData = [
    {
        title: "Stage 1 | Multi-Class Classification",
        subtitle: "Building the Supervised Learning Pipeline",
        markdown: `The initial phase focuses on developing a high-fidelity classifier using the CIC-DDoS2019 dataset. We implemented a technical workflow involving Label Normalization (merging benign and attack sub-categories) and a Stratified 80/20 Train-Test Split. The core engine is a Random Forest Ensemble trained to categorize traffic into four distinct behavioral classes: Benign, SYN Flood, LDAP Reflection, and UDP Volumetric attacks.`,
        outputTitle: "Phase 1: Laboratory Metrics",
        accuracy: "99.87%",
        secondaryLabel: "Algorithm",
        secondaryValue: "Random Forest",
        recall: "99.8%",
        image: "/static/img/confusion_matrix.png"
    },
    {
        title: "Stage 2 | Robustness Audit",
        subtitle: "Leakage Detection & Feature Selection",
        markdown: `Exposing laboratory artifacts is critical for model integrity. We performed a Feature Importance Analysis which identified high-leakage parameters like Init Fwd Win Bytes. These features often contain static values inherent to lab environments rather than malicious behavior. By excluding these identity-biased artifacts, we developed a Hardened Model that relies purely on behavioral timing and volume metrics.`,
        outputTitle: "Phase 2: Audit Results",
        accuracy: "99.70%",
        secondaryLabel: "Audit Status",
        secondaryValue: "Leaks Mitigated",
        recall: "99.2%",
        image: "/static/img/feature_importance.png"
    },
    {
        title: "Stage 3 | Generalization Test",
        subtitle: "Cross-Environment Performance Analysis",
        markdown: `To evaluate real-world utility, the model was subjected to a Zero-Shot Test against an external network dataset. This revealed a significant Generalization Gap: while the model maintained high precision for benign traffic, the botnet detection recall dropped to approximately 3%. This identified a Model Blindness to attack patterns outside of its primary training environment, necessitating a more diverse data strategy.`,
        outputTitle: "Phase 3: Reality Stress Test",
        accuracy: "81.02%",
        secondaryLabel: "Detection Gap",
        secondaryValue: "Model Blindness",
        recall: "95% (Benign)",
        image: "/static/img/confusion_matrix.png"
    },
    {
        title: "Stage 4 | Universal Brain",
        subtitle: "Dataset Fusion & Global Deployment",
        markdown: `The final stage leverages Dataset Fusion to create a robust, network-agnostic detector. We merged the deep laboratory data with external samples and standardized them into a Unified Behavioral Schema. This Universal Brain generalizes across different network signatures, effectively identifying botnets regardless of their network origin or specific environment artifacts.`,
        outputTitle: "Phase 4: Unified Evaluation",
        accuracy: "99.87%",
        secondaryLabel: "Deployment",
        secondaryValue: "Universal (Agonstic)",
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
            <h2 style="font-size: 1.6rem;"><span style="color: var(--accent-color)">#</span> ${data.title}</h2>
            <p class="markdown-text" style="font-weight: 700; color: var(--accent-color); margin-bottom: 20px; text-transform: uppercase; letter-spacing: 1px;">${data.subtitle}</p>
            <p class="markdown-text" style="font-size: 1.1rem; line-height: 1.8;">${data.markdown}</p>
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

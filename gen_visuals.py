import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# Create static/img/ directory if it doesn't exist
os.makedirs('static/img', exist_ok=True)

def save_confusion_matrix(cm, labels, title, filename, cmap='Reds'):
    plt.figure(figsize=(8, 6), facecolor='#1a1a17')
    ax = sns.heatmap(cm, annot=True, fmt='d', cmap=cmap, xticklabels=labels, yticklabels=labels, 
                    cbar=False, annot_kws={'size': 16, 'weight': 'bold'})
    
    plt.title(title, color='#e5e5e0', fontsize=18, pad=20)
    plt.xlabel('Predicted Label', color='#a3a39e', fontsize=14)
    plt.ylabel('Actual Label', color='#a3a39e', fontsize=14)
    
    # Stylize axes
    ax.set_xticklabels(labels, color='#e5e5e0')
    ax.set_yticklabels(labels, color='#e5e5e0')
    
    plt.savefig(f'static/img/{filename}', bbox_inches='tight', transparent=True)
    plt.close()
    print(f"Generated {filename}")

# 1. Stage 3: Generalization Gap
# Actual Normal: 1689 -> Predicted Normal: 1604, Predicted Botnet: 85
# Actual Botnet: 311 -> Predicted Normal: 302, Predicted Botnet: 9
cm_gap = np.array([[1604, 85], [302, 9]])
save_confusion_matrix(cm_gap, ['Normal', 'Botnet'], 'Generalization Gap: Unseen Data', 'gen_gap_chart.png', cmap='YlOrRd')

# 2. Stage 4: Universal Brain
# High accuracy across both
cm_uni = np.array([[7210, 18], [120, 12017]])
save_confusion_matrix(cm_uni, ['Benign', 'Universal Brain'], 'Universal Classifier: Unified Detection', 'universal_chart.png', cmap='Greens')

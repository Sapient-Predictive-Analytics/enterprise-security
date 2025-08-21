import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import seaborn as sns
from matplotlib.patches import Circle
from scipy.ndimage import gaussian_filter
import random

# Set style for professional appearance
plt.style.use('dark_background')

# Create figure with dark theme and better spacing
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(20, 16))
fig.patch.set_facecolor('#0a0a0a')

# Enhanced main title with proper spacing
fig.suptitle('CARDANO ENTERPRISE CYBERSECURITY AI\nThreat Detection & Network Analysis Dashboard', 
             fontsize=24, color='#cc2936', fontweight='bold', y=0.96)

# Corporate color palette - burgundy, matte purple, gunmetal
colors_corporate = ['#8b1538', '#6b4c57', '#4a5568', '#2d3748', '#1a202c']
burgundy = '#8b1538'
matte_purple = '#6b4c57'
gunmetal = '#4a5568'
dark_slate = '#2d3748'

# 1. Threat Correlation Network (Top Left) - Enhanced
ax1.set_facecolor('#0a0a0a')
G = nx.Graph()

# Define threat categories and relationships
threat_nodes = {
    'Web2/Web3 Bridge': {'type': 'critical', 'severity': 9},
    'Cross-Site Scripting': {'type': 'web', 'severity': 7},
    'Phishing Attacks': {'type': 'social', 'severity': 8},
    'DNS Hijacking': {'type': 'network', 'severity': 8},
    'Server Vulnerabilities': {'type': 'infrastructure', 'severity': 9},
    'Wallet Integration': {'type': 'blockchain', 'severity': 8},
    'Smart Contract Interface': {'type': 'blockchain', 'severity': 7},
    'API Endpoints': {'type': 'web', 'severity': 6},
    'Database Injection': {'type': 'web', 'severity': 8},
    'Man-in-Middle': {'type': 'network', 'severity': 7},
    'Session Hijacking': {'type': 'web', 'severity': 6},
    'DDoS Attacks': {'type': 'network', 'severity': 5},
    'Social Engineering': {'type': 'social', 'severity': 7},
    'Insider Threats': {'type': 'internal', 'severity': 6}
}

# Add nodes to graph
for node, attrs in threat_nodes.items():
    G.add_node(node, **attrs)

# Create realistic threat relationships
threat_edges = [
    ('Web2/Web3 Bridge', 'Wallet Integration', 0.9),
    ('Web2/Web3 Bridge', 'Smart Contract Interface', 0.8),
    ('Cross-Site Scripting', 'API Endpoints', 0.7),
    ('Cross-Site Scripting', 'Session Hijacking', 0.8),
    ('Phishing Attacks', 'Social Engineering', 0.9),
    ('Phishing Attacks', 'Wallet Integration', 0.6),
    ('DNS Hijacking', 'Man-in-Middle', 0.8),
    ('Server Vulnerabilities', 'Database Injection', 0.7),
    ('Server Vulnerabilities', 'API Endpoints', 0.8),
    ('API Endpoints', 'Database Injection', 0.6),
    ('DDoS Attacks', 'Server Vulnerabilities', 0.5),
    ('Insider Threats', 'Database Injection', 0.4),
    ('Social Engineering', 'Insider Threats', 0.5)
]

for edge in threat_edges:
    G.add_edge(edge[0], edge[1], weight=edge[2])

# Position nodes using spring layout
pos = nx.spring_layout(G, k=3, iterations=50, seed=42)

# Enhanced edge drawing with gradient effect
for edge in G.edges(data=True):
    x1, y1 = pos[edge[0]]
    x2, y2 = pos[edge[1]]
    alpha = edge[2]['weight']
    width = alpha * 3
    ax1.plot([x1, x2], [y1, y2], color=gunmetal, alpha=alpha*0.8, linewidth=width)

# Enhanced node coloring with corporate palette
severity_colors = []
node_sizes = []
for node in G.nodes():
    severity = threat_nodes[node]['severity']
    if severity >= 8:
        severity_colors.append(burgundy)
    elif severity >= 6:
        severity_colors.append(matte_purple)
    else:
        severity_colors.append(gunmetal)
    node_sizes.append(severity * 250)

# Draw nodes with enhanced styling
scatter = ax1.scatter([pos[node][0] for node in G.nodes()], 
                     [pos[node][1] for node in G.nodes()],
                     c=severity_colors, s=node_sizes, alpha=0.9, 
                     edgecolors='white', linewidth=3)

# Add labels for key nodes
key_nodes = ['Web2/Web3 Bridge', 'Phishing Attacks', 'Server Vulnerabilities', 'DNS Hijacking']
for node in key_nodes:
    x, y = pos[node]
    ax1.annotate(node, (x, y), xytext=(5, 5), textcoords='offset points',
                fontsize=10, color='white', fontweight='bold',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='black', alpha=0.7))

ax1.set_title('Threat Correlation Network\nAI-Powered Relationship Analysis', 
              color=burgundy, fontsize=14, fontweight='bold', pad=20)
ax1.axis('off')

# 2. Real-time Threat Detection (Top Right) - Enhanced with markers
ax2.set_facecolor('#0a0a0a')

# Simulate real-time threat detection data
time_points = np.arange(0, 24, 0.5)
threats = {
    'XSS Attempts': np.random.poisson(3, len(time_points)) + np.sin(time_points/2) * 2,
    'Phishing Emails': np.random.poisson(2, len(time_points)) + np.cos(time_points/3) * 1.5,
    'DNS Anomalies': np.random.poisson(1, len(time_points)) + np.random.exponential(0.5, len(time_points)),
    'API Attacks': np.random.poisson(4, len(time_points)) + np.sin(time_points/4) * 3
}

# Corporate colors for line chart
line_colors = [burgundy, matte_purple, gunmetal, dark_slate]
line_styles = ['-', '--', '-.', ':']
markers = ['o', '^', 's', 'D']

# Plot enhanced lines with markers
for i, (threat_name, threat_data) in enumerate(threats.items()):
    ax2.plot(time_points, threat_data, color=line_colors[i], 
             linestyle=line_styles[i], linewidth=3, alpha=0.8,
             marker=markers[i], markersize=4, markevery=4,
             label=threat_name)

ax2.set_xlabel('Time (Hours)', color='white', fontsize=12)
ax2.set_ylabel('Threat Count', color='white', fontsize=12)
ax2.set_title('Real-Time Threat Detection\nAI Anomaly Identification', 
              color=burgundy, fontsize=14, fontweight='bold', pad=20)
ax2.legend(loc='upper left', facecolor='#1a1a1a', edgecolor=gunmetal, 
           framealpha=0.9, fontsize=10)
ax2.grid(True, alpha=0.2, color=gunmetal)
ax2.set_facecolor('#0f0f0f')

# 3. Enhanced Vulnerability Heatmap with smoothing
ax3.set_facecolor('#0a0a0a')

# Create vulnerability matrix
vulnerabilities = ['XSS', 'CSRF', 'SQL Inj', 'DNS Hijack', 'DDoS', 'Phishing', 'MITM', 'Session']
systems = ['Web Portal', 'API Gateway', 'Database', 'Wallet IF', 'Smart Contracts', 'DNS Server']

# Generate realistic vulnerability scores
np.random.seed(42)
vuln_matrix = np.random.beta(2, 5, (len(systems), len(vulnerabilities))) * 10

# Add some realistic patterns
vuln_matrix[0, 0] = 8.5  # Web Portal - XSS
vuln_matrix[0, 1] = 7.2  # Web Portal - CSRF
vuln_matrix[1, 0] = 6.8  # API Gateway - XSS
vuln_matrix[2, 2] = 9.1  # Database - SQL Injection
vuln_matrix[3, 5] = 8.9  # Wallet Interface - Phishing
vuln_matrix[5, 3] = 9.3  # DNS Server - DNS Hijack

# Apply Gaussian smoothing for diffusion effect
vuln_matrix_smooth = gaussian_filter(vuln_matrix, sigma=0.5)

# Create custom colormap from burgundy to light gray
from matplotlib.colors import LinearSegmentedColormap
colors_heatmap = ['#1a1a1a', '#4a1e2a', '#6b2c3e', '#8b1538', '#a03d52', '#c46b7a']
n_bins = 100
cmap_custom = LinearSegmentedColormap.from_list('custom_burgundy', colors_heatmap, N=n_bins)

# Create enhanced heatmap
heatmap = ax3.imshow(vuln_matrix_smooth, cmap=cmap_custom, aspect='auto', alpha=0.9,
                    interpolation='bilinear')

# Add text annotations with better formatting
for i in range(len(systems)):
    for j in range(len(vulnerabilities)):
        value = vuln_matrix[i, j]
        color = 'white' if value < 5 else 'black'
        text = ax3.text(j, i, f'{value:.1f}', 
                       ha="center", va="center", color=color, 
                       fontweight='bold', fontsize=11)

ax3.set_xticks(range(len(vulnerabilities)))
ax3.set_yticks(range(len(systems)))
ax3.set_xticklabels(vulnerabilities, rotation=45, ha='right', color='white', fontsize=11)
ax3.set_yticklabels(systems, color='white', fontsize=11)
ax3.set_title('Vulnerability Assessment Matrix\nAI Risk Scoring', 
              color=burgundy, fontsize=14, fontweight='bold', pad=20)

# Enhanced colorbar
cbar = plt.colorbar(heatmap, ax=ax3, fraction=0.046, pad=0.04)
cbar.set_label('Risk Score', color='white', fontsize=12)
cbar.ax.yaxis.set_tick_params(color='white')

# 4. Enhanced Attack Vector Analysis
ax4.set_facecolor('#0a0a0a')

# Create attack vector data
attack_vectors = ['External\nAttackers', 'Malicious\nInsiders', 'Third-Party\nCompromise', 
                 'Supply Chain\nAttacks', 'Social\nEngineering', 'Automated\nBots']
attack_counts = [45, 12, 23, 8, 34, 67]

# Corporate color palette for pie chart
colors_pie = [burgundy, matte_purple, gunmetal, dark_slate, '#5a4a5a', '#3a3a4a']

# Create enhanced pie chart
wedges, texts, autotexts = ax4.pie(attack_counts, labels=attack_vectors, colors=colors_pie,
                                  autopct='%1.1f%%', startangle=90, textprops={'color': 'white'},
                                  wedgeprops=dict(edgecolor='white', linewidth=2))

# Enhance pie chart appearance
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')
    autotext.set_fontsize(11)

for text in texts:
    text.set_fontsize(10)
    text.set_fontweight('bold')

ax4.set_title('Attack Vector Distribution\nAI Threat Classification', 
              color=burgundy, fontsize=14, fontweight='bold', pad=20)

# Enhanced styling for all plots
for ax in [ax1, ax2, ax3, ax4]:
    ax.tick_params(colors='white', labelsize=10)

# Enhanced footer with better spacing
footer_text = "AI-Powered Analysis: Real-time threat correlation • Behavioral anomaly detection • Predictive risk assessment • Automated response recommendations"
fig.text(0.5, 0.01, footer_text, ha='center', va='bottom', 
         fontsize=12, color='#888888', style='italic')

plt.tight_layout()
plt.subplots_adjust(top=0.89, bottom=0.06, hspace=0.3, wspace=0.25)

# Save with high quality
plt.savefig('cardano_cybersecurity_threat_analysis.png', dpi=300, bbox_inches='tight', 
            facecolor='#0a0a0a', edgecolor='none', pad_inches=0.3)
plt.show()

print("Enhanced cybersecurity threat analysis dashboard saved as 'cardano_cybersecurity_threat_analysis.png'")
print("Features: Corporate color palette, smooth heatmap, enhanced line chart, professional spacing")
"""
Figure 4.4 – E-government and university-online service access patterns by university type
"""
import pandas as pd, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

COLORS = {'Public': '#0B3D5B', 'Private': '#1A6B9C', 'NU': '#5B8FB9'}
TYPES  = {1: 'Public', 2: 'Private', 3: 'NU'}

df = pd.read_csv('../data_cleaned.csv')
df.replace(-99, np.nan, inplace=True)

# Grouped bar: % who have used e-gov services vs. % whose uni provides online services
labels = ['Used e-gov\nservices (≥once)', 'Uni provides\nonline services']
x = np.arange(len(labels))
width = 0.25

fig, ax = plt.subplots(figsize=(7, 5))
fig.patch.set_facecolor('#FFFFFF')
ax.set_facecolor('#FFFFFF')

for i, (t, name) in enumerate(TYPES.items()):
    sub = df[df.A2_Type == t]
    v1 = (sub['B3.1_EGovUse'].isin([1, 2, 3])).sum() / sub['B3.1_EGovUse'].notna().sum() * 100
    v2 = (sub['B3.4_UniOnlineYes'] == 1).sum() / len(sub) * 100
    ax.bar(x + (i - 1) * width, [v1, v2], width,
           label=name, color=COLORS[name], zorder=3)

ax.set_ylabel('Percentage (%)', fontsize=11, color='#1A1A1A')
ax.set_xticks(x)
ax.set_xticklabels(labels, fontsize=10, color='#1A1A1A')
ax.set_ylim(0, 105)
ax.yaxis.grid(True, color='#B5C7D9', linewidth=0.6, zorder=0)
ax.set_axisbelow(True)
ax.spines[['top', 'right']].set_visible(False)
ax.spines[['left', 'bottom']].set_color('#B5C7D9')
ax.tick_params(colors='#1A1A1A')
ax.legend(frameon=False, fontsize=10)

plt.tight_layout()
plt.savefig('figure_4_4_egovernment.png', dpi=300, bbox_inches='tight',
            facecolor='white')
plt.close()
print("Saved: figure_4_4_egovernment.png")

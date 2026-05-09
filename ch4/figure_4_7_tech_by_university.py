"""
Figure 4.7 – Distribution of tech_total by university type
Box plot with individual jitter + diamond = mean (Ocean Depths palette)
"""
import pandas as pd, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

COLORS = {'Public': '#0B3D5B', 'Private': '#1A6B9C', 'NU': '#5B8FB9'}
TYPES  = {1: 'Public', 2: 'Private', 3: 'NU'}

df = pd.read_csv('../data_cleaned.csv')
df.replace(-99, np.nan, inplace=True)

groups = [df[df.A2_Type == t]['tech_total'].dropna().values for t in TYPES]
labels = list(TYPES.values())
colors = [COLORS[n] for n in labels]

fig, ax = plt.subplots(figsize=(7, 5.5))
fig.patch.set_facecolor('#FFFFFF')
ax.set_facecolor('#FFFFFF')

bp = ax.boxplot(groups, positions=[1, 2, 3], widths=0.45,
                patch_artist=True, notch=False,
                medianprops=dict(color='#FFFFFF', linewidth=2),
                whiskerprops=dict(color='#1A1A1A', linewidth=1.2),
                capprops=dict(color='#1A1A1A', linewidth=1.2),
                flierprops=dict(marker='o', markersize=3,
                                markerfacecolor='#B5C7D9', alpha=0.5))

for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.85)

# Diamond = mean
for i, (g, color) in enumerate(zip(groups, colors), start=1):
    ax.scatter(i, np.mean(g), marker='D', s=60, color='#F4A261',
               zorder=5, label='Mean' if i == 1 else '')

# Jitter
np.random.seed(42)
for i, (g, color) in enumerate(zip(groups, colors), start=1):
    jitter = np.random.uniform(-0.15, 0.15, size=len(g))
    ax.scatter(i + jitter, g, alpha=0.15, s=8, color=color, zorder=2)

ax.set_xticks([1, 2, 3])
ax.set_xticklabels(labels, fontsize=11, color='#1A1A1A')
ax.set_ylabel('tech_total composite score', fontsize=11, color='#1A1A1A')
ax.set_ylim(0.20, 0.68)
ax.yaxis.grid(True, color='#B5C7D9', linewidth=0.6, zorder=0)
ax.set_axisbelow(True)
ax.spines[['top', 'right']].set_visible(False)
ax.spines[['left', 'bottom']].set_color('#B5C7D9')
ax.tick_params(colors='#1A1A1A')
ax.legend(frameon=False, fontsize=10)

plt.tight_layout()
plt.savefig('figure_4_7_tech_by_university.png', dpi=300, bbox_inches='tight',
            facecolor='white')
plt.close()
print("Saved: figure_4_7_tech_by_university.png")
for t, name in TYPES.items():
    g = df[df.A2_Type == t]['tech_total'].dropna()
    print(f"  {name}: M={g.mean():.3f}, SD={g.std():.3f}, n={len(g)}")

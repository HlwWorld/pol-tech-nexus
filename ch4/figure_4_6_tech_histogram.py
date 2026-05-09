"""
Figure 4.6 – Histogram of the tech_total composite with kernel density overlay (n = 472)
"""
import pandas as pd, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

df = pd.read_csv('../data_cleaned.csv')
df.replace(-99, np.nan, inplace=True)
data = df['tech_total'].dropna().values

fig, ax = plt.subplots(figsize=(8, 5))
fig.patch.set_facecolor('#FFFFFF')
ax.set_facecolor('#FFFFFF')

# Histogram
n, bins, patches = ax.hist(data, bins=20, density=True,
                            color='#5B8FB9', alpha=0.75, edgecolor='#FFFFFF',
                            linewidth=0.5, zorder=3)

# KDE overlay
kde = gaussian_kde(data, bw_method='scott')
x_range = np.linspace(data.min() - 0.01, data.max() + 0.01, 300)
ax.plot(x_range, kde(x_range), color='#0B3D5B', linewidth=2.0, zorder=4)

# Mean line
ax.axvline(data.mean(), color='#F4A261', linewidth=1.5, linestyle='--', zorder=5,
           label=f'Mean = {data.mean():.3f}')

ax.set_xlabel('tech_total composite score', fontsize=11, color='#1A1A1A')
ax.set_ylabel('Density', fontsize=11, color='#1A1A1A')
ax.tick_params(colors='#1A1A1A')
ax.spines[['top', 'right']].set_visible(False)
ax.spines[['left', 'bottom']].set_color('#B5C7D9')
ax.yaxis.grid(True, color='#B5C7D9', linewidth=0.6, zorder=0)
ax.set_axisbelow(True)
ax.legend(frameon=False, fontsize=10)

plt.tight_layout()
plt.savefig('figure_4_6_tech_histogram.png', dpi=300, bbox_inches='tight',
            facecolor='white')
plt.close()
print(f"Saved: figure_4_6_tech_histogram.png  "
      f"(M={data.mean():.3f}, SD={data.std():.3f}, "
      f"skew={pd.Series(data).skew():.3f})")

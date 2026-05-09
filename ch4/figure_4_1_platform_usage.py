"""
Figure 4.1 – Social media platform usage distribution by university type
Ocean Depths palette: Public=#0B3D5B, Private=#1A6B9C, NU College=#5B8FB9
Note: 1 non-user (B1.1_11_None == 1) excluded; n = 471.
"""
import pandas as pd, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

COLORS = {'Public': '#0B3D5B', 'Private': '#1A6B9C', 'NU College': '#5B8FB9'}
TYPES  = {1: 'Public', 2: 'Private', 3: 'NU College'}

# ---------------------------------------------------------------
# Load data and exclude non-user(s)
# ---------------------------------------------------------------
df = pd.read_csv('data_cleaned.csv')
df.replace(-99, np.nan, inplace=True)
df = df[df['B1.1_11_None'] != 1].copy()   # exclude non-users (n_excluded = 1)

# ---------------------------------------------------------------
# Platforms (ordered by overall popularity, descending)
# ---------------------------------------------------------------
PLATFORMS = [
    ('B1.1_1_Facebook',   'Facebook'),
    ('B1.1_4_WhatsApp',   'WhatsApp'),
    ('B1.1_6_YouTube',    'YouTube'),
    ('B1.1_3_Instagram',  'Instagram'),
    ('B1.1_7_TikTok',     'TikTok'),
    ('B1.1_5_Telegram',   'Telegram'),
    ('B1.1_2_X',          'X (Twitter)'),
    ('B1.1_8_LinkedIn',   'LinkedIn'),
]
labels = [p[1] for p in PLATFORMS]
x = np.arange(len(labels))
width = 0.25

# ---------------------------------------------------------------
# Plot
# ---------------------------------------------------------------
fig, ax = plt.subplots(figsize=(11, 5.5))
fig.patch.set_facecolor('#FFFFFF')
ax.set_facecolor('#FFFFFF')

for i, (code, name) in enumerate(TYPES.items()):
    sub  = df[df['A2_Type'] == code]
    vals = [sub[c].mean() * 100 for c, _ in PLATFORMS]
    ax.bar(x + (i - 1) * width, vals, width,
           label=f"{name} (n={len(sub)})",
           color=COLORS[name], zorder=3)

ax.set_ylabel('Percentage using platform (%)', fontsize=11,
              color='#1A1A1A', fontfamily='DejaVu Sans')
ax.set_xticks(x)
ax.set_xticklabels(labels, fontsize=10, color='#1A1A1A')
ax.set_ylim(0, 105)
ax.yaxis.grid(True, color='#B5C7D9', linewidth=0.6, zorder=0)
ax.set_axisbelow(True)
ax.spines[['top', 'right']].set_visible(False)
ax.spines[['left', 'bottom']].set_color('#B5C7D9')
ax.tick_params(colors='#1A1A1A')
ax.legend(frameon=False, fontsize=10, labelcolor='#1A1A1A')

plt.tight_layout()
plt.savefig('figure_4_1_platform_usage.png', dpi=300,
            bbox_inches='tight', facecolor='white')
plt.close()
print("Saved: figure_4_1_platform_usage.png")

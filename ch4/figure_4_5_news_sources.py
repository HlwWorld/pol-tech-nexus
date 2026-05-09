"""
Figure 4.5 – Online news source preferences by university type
"""
import pandas as pd, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

COLORS = {'Public': '#0B3D5B', 'Private': '#1A6B9C', 'NU': '#5B8FB9'}
TYPES  = {1: 'Public', 2: 'Private', 3: 'NU'}

SOURCE_COLS = [
    ('B4.3_1_BDNewspapers',   'BD Newspapers'),
    ('B4.3_7_OnlinePortals',  'Online Portals'),
    ('B4.3_3_BDYouTubeNews',  'BD YouTube News'),
    ('B4.3_2_IntNews',        'Intl News Sites'),
    ('B4.3_5_Aggregators',    'Aggregators'),
    ('B4.3_4_IntYouTubeNews', 'Intl YouTube'),
    ('B4.3_6_Podcasts',       'Podcasts'),
]

df = pd.read_csv('../data_cleaned.csv')
df.replace(-99, np.nan, inplace=True)

labels = [s[1] for s in SOURCE_COLS]
x = np.arange(len(labels))
width = 0.25

fig, ax = plt.subplots(figsize=(11, 5))
fig.patch.set_facecolor('#FFFFFF')
ax.set_facecolor('#FFFFFF')

for i, (t, name) in enumerate(TYPES.items()):
    sub  = df[df.A2_Type == t]
    vals = [sub[c].mean() * 100 for c, _ in SOURCE_COLS]
    ax.bar(x + (i - 1) * width, vals, width,
           label=name, color=COLORS[name], zorder=3)

ax.set_ylabel('Percentage (%)', fontsize=11, color='#1A1A1A')
ax.set_xticks(x)
ax.set_xticklabels(labels, fontsize=9, color='#1A1A1A', rotation=15, ha='right')
ax.set_ylim(0, 105)
ax.yaxis.grid(True, color='#B5C7D9', linewidth=0.6, zorder=0)
ax.set_axisbelow(True)
ax.spines[['top', 'right']].set_visible(False)
ax.spines[['left', 'bottom']].set_color('#B5C7D9')
ax.tick_params(colors='#1A1A1A')
ax.legend(frameon=False, fontsize=10)

plt.tight_layout()
plt.savefig('figure_4_5_news_sources.png', dpi=300, bbox_inches='tight',
            facecolor='white')
plt.close()
print("Saved: figure_4_5_news_sources.png")

"""
Figure 4.2 – Daily time spent on social media by university type (stacked bar)
Ocean Depths palette
"""
import pandas as pd, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

TIME_LABELS = {
    1: '<30 min', 2: '30m–1h', 3: '1–2h',
    4: '2–3h', 5: '3–4h', 6: '>4h',
}
COLORS = ['#C8DCEC', '#5B8FB9', '#1A6B9C', '#0B3D5B', '#356A8C', '#F4A261']
TYPES  = {1: 'Public', 2: 'Private', 3: 'NU'}

df = pd.read_csv('../data_cleaned.csv')
df.replace(-99, np.nan, inplace=True)

fig, ax = plt.subplots(figsize=(8, 5))
fig.patch.set_facecolor('#FFFFFF')
ax.set_facecolor('#FFFFFF')

x = np.arange(len(TYPES))
bottoms = np.zeros(3)

for ci, (code, label) in enumerate(TIME_LABELS.items()):
    vals = []
    for t in TYPES:
        sub = df[df.A2_Type == t]['B1.2_TimeSocial']
        valid = sub.notna().sum()
        n = (sub == code).sum()
        vals.append(n / valid * 100 if valid > 0 else 0)
    ax.bar(x, vals, 0.55, bottom=bottoms,
           label=label, color=COLORS[ci], zorder=3)
    bottoms += np.array(vals)

ax.set_xticks(x)
ax.set_xticklabels(list(TYPES.values()), fontsize=11, color='#1A1A1A')
ax.set_ylabel('Percentage of respondents (%)', fontsize=11, color='#1A1A1A')
ax.set_ylim(0, 105)
ax.yaxis.grid(True, color='#B5C7D9', linewidth=0.6, zorder=0)
ax.set_axisbelow(True)
ax.spines[['top', 'right']].set_visible(False)
ax.spines[['left', 'bottom']].set_color('#B5C7D9')
ax.tick_params(colors='#1A1A1A')
ax.legend(title='Daily time', frameon=False, fontsize=9,
          bbox_to_anchor=(1.01, 1), loc='upper left')

plt.tight_layout()
plt.savefig('figure_4_2_social_media_time.png', dpi=300, bbox_inches='tight',
            facecolor='white')
plt.close()
print("Saved: figure_4_2_social_media_time.png")

"""
Figure 4.3 – Messaging app usage by university type
"""
import pandas as pd, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

COLORS = {'Public': '#0B3D5B', 'Private': '#1A6B9C', 'NU': '#5B8FB9'}
TYPES  = {1: 'Public', 2: 'Private', 3: 'NU'}

APP_COLS = [
    ('B2.1_1_FBMessenger', 'FB Messenger'),
    ('B2.1_2_WhatsApp',    'WhatsApp'),
    ('B2.1_3_Telegram',    'Telegram'),
    ('B2.1_4_Viber',       'Viber'),
    ('B2.1_5_IMO',         'IMO'),
    ('B2.1_6_Signal',      'Signal'),
]

df = pd.read_csv('../data_cleaned.csv')
df.replace(-99, np.nan, inplace=True)

labels = [a[1] for a in APP_COLS]
x = np.arange(len(labels))
width = 0.25

fig, ax = plt.subplots(figsize=(9, 5))
fig.patch.set_facecolor('#FFFFFF')
ax.set_facecolor('#FFFFFF')

for i, (t, name) in enumerate(TYPES.items()):
    sub  = df[df.A2_Type == t]
    vals = [sub[c].mean() * 100 for c, _ in APP_COLS]
    ax.bar(x + (i - 1) * width, vals, width,
           label=name, color=COLORS[name], zorder=3)

ax.set_ylabel('Percentage using app (%)', fontsize=11, color='#1A1A1A')
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
plt.savefig('figure_4_3_messaging_usage.png', dpi=300, bbox_inches='tight',
            facecolor='white')
plt.close()
print("Saved: figure_4_3_messaging_usage.png")

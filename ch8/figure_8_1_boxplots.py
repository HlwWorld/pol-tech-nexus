"""
================================================================
SCRIPT: figure_8_1_boxplots.py
================================================================
PURPOSE:
    Produce a 2x2 panel of box plots comparing the distribution
    of each of the four key composite variables across the three
    university types, providing the visual companion to the
    ANOVA results.

OUTPUT:
    Thesis Figure 8.1, Box Plots of Key Variables by University Type
    Four panels: tech_total, internal_eff, external_eff, engagement.

HYPOTHESIS TESTED: H4 (visualization)

THESIS REFERENCE:
    Chapter 8, Section 8.6, Visualization of Disparities

INPUT:
    data_cleaned.csv

METHOD:
    Grouped box plots (matplotlib), Ocean Depths figure palette,
    group means overlaid as diamond markers.

DEPENDENCIES:
    pandas, numpy, matplotlib

================================================================
The code is made available only for academic purposes and
verification. Redistribution, reuse, or modification of this
code, in its entirety or in part, will require the author's
written permission.
================================================================
"""

import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif']

df = pd.read_csv("data_cleaned.csv")
df = df.replace(-99, float('nan'))   # valid skip -> NaN for analysis

df['Type'] = df['A2_Type'].map({1: 'Public', 2: 'Private', 3: 'NU'})
order = ['Public', 'Private', 'NU']
colors = {'Public': '#0B3D5B', 'Private': '#1A6B9C', 'NU': '#5B8FB9'}
panels = [('tech_total', 'Technological Advancement\n(composite, 0-1)'),
          ('internal_eff', 'Internal Political Efficacy\n(mean, 1-5)'),
          ('external_eff', 'External Political Efficacy\n(mean, 1-5)'),
          ('engagement', 'Political Engagement\n(composite, 1-5)')]

fig, axes = plt.subplots(2, 2, figsize=(8.0, 7.2))
axes = axes.ravel()
for ax, (dv, title) in zip(axes, panels):
    data = [df.loc[df['Type'] == t, dv].dropna().values for t in order]
    bp = ax.boxplot(data, patch_artist=True, widths=0.55, showmeans=True,
                    medianprops=dict(color='#F4A261', linewidth=1.8),
                    meanprops=dict(marker='D', markerfacecolor='#F4A261',
                                   markeredgecolor='#1A1A1A', markersize=5))
    for patch, t in zip(bp['boxes'], order):
        patch.set_facecolor(colors[t])
        patch.set_edgecolor('#1A1A1A')
        patch.set_alpha(0.88)
    ax.set_xticklabels(order)
    ax.set_title(title, fontweight='bold', color='#0B3D5B')
    ax.grid(axis='y', color='#B5C7D9', linewidth=0.6, alpha=0.7)
    ax.set_axisbelow(True)

legend = [Patch(facecolor=colors[t], edgecolor='#1A1A1A', label=t) for t in order]
fig.legend(handles=legend, loc='lower center', ncol=3, frameon=False)
fig.tight_layout(rect=[0, 0.045, 1, 1])
fig.savefig('figure_8_1_boxplots.png', dpi=200, bbox_inches='tight',
            facecolor='white')

"""
================================================================
SCRIPT: figure_8_1_boxplots.py
================================================================
PURPOSE:
    Visualize the distribution of the four key composite variables
    across the three university types using side-by-side box plots,
    making the location, spread, and overlap of each group's scores
    visible at a glance in support of the H4 analysis.

OUTPUT:
    Thesis Figure 8.1, Box Plots of Key Variables by University Type
    Produces a 2x2 panel of box plots (tech_total, internal_eff,
    external_eff, engagement) grouped by university type.

HYPOTHESIS TESTED: H4

THESIS REFERENCE:
    Chapter 8, Section 8.6, Visualization of Disparities

INPUT:
    data_cleaned.csv

METHOD:
    matplotlib boxplot, group means overlaid as diamond markers,
    Ocean Depths figure palette (Section 16.10).

DEPENDENCIES:
    pandas, numpy, matplotlib

================================================================
The code is made available only for academic purposes and
verification. Redistribution, reuse, or modification of this
code, in its entirety or in part, will require the author's
written permission.
================================================================
"""

import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "utilities"))
from plot_styles import apply_house_style, TYPE_COLORS, TYPE_ORDER, OCEAN

apply_house_style()

df = pd.read_csv("data_cleaned.csv")
df = df.replace(-99, float('nan'))  # valid skip -> NaN for analysis
df["UniType"] = df["A2_Type"].map({1: "Public", 2: "Private", 3: "NU"})

PANELS = [
    ("tech_total",   "Technological Advancement", "Composite score (0-1)"),
    ("internal_eff", "Internal Political Efficacy", "Mean score (1-5)"),
    ("external_eff", "External Political Efficacy", "Mean score (1-5)"),
    ("engagement",   "Political Engagement",       "Mean score (1-5)"),
]

fig, axes = plt.subplots(2, 2, figsize=(9.2, 7.4))
axes = axes.ravel()

for ax, (var, title, ylab) in zip(axes, PANELS):
    data = [df.loc[df["UniType"] == t, var].dropna().values for t in TYPE_ORDER]
    bp = ax.boxplot(data, patch_artist=True, widths=0.55,
                    medianprops=dict(color=OCEAN["ink"], linewidth=1.4),
                    whiskerprops=dict(color=OCEAN["ink"], linewidth=1.0),
                    capprops=dict(color=OCEAN["ink"], linewidth=1.0),
                    flierprops=dict(marker="o", markersize=3,
                                    markerfacecolor="none",
                                    markeredgecolor=OCEAN["ink"], alpha=0.5))
    for patch, color in zip(bp["boxes"], TYPE_COLORS):
        patch.set_facecolor(color)
        patch.set_edgecolor(OCEAN["ink"])
        patch.set_alpha(0.85)
    # overlay group means as orange diamonds
    means = [np.nanmean(d) for d in data]
    ax.scatter(range(1, len(means) + 1), means, marker="D", s=42,
               color=OCEAN["orange"], edgecolor=OCEAN["ink"],
               zorder=5, label="Group mean")
    ax.set_xticks(range(1, len(TYPE_ORDER) + 1))
    ax.set_xticklabels(TYPE_ORDER)
    ax.set_title(title, fontsize=11.5, pad=8)
    ax.set_ylabel(ylab, fontsize=10)
    ax.grid(axis="x", visible=False)

handles, labels = axes[0].get_legend_handles_labels()
fig.legend(handles, labels, loc="lower center", ncol=1, frameon=False,
           fontsize=9, bbox_to_anchor=(0.5, -0.01))
fig.tight_layout(rect=[0, 0.03, 1, 1])
fig.savefig("figures/figure_8_1_boxplots.png", dpi=300, bbox_inches="tight")
print("Saved figures/figure_8_1_boxplots.png")

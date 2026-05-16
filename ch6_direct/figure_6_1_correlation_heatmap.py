"""
================================================================
SCRIPT      : figure_6_1_correlation_heatmap.py
PURPOSE     : Produce a 4x4 correlation heatmap of tech_total,
              engagement, internal_eff, and external_eff using
              the Ocean Depths color palette.
OUTPUT      : Figure 6.1 - Correlation Heatmap
HYPOTHESIS  : H1 (visual support)
THESIS REF  : Chapter 6, Section 6.2, Examining Direct Relationships
INPUT       : data_cleaned.csv (n = 472)
METHOD      : Pearson correlation; matplotlib imshow with a custom
              diverging colormap (red -> white -> deep ocean).
DEPENDENCIES: pandas, numpy, matplotlib
================================================================
Copyright (c) 2026. All rights reserved.
Academic use only; explicit written permission required for reuse.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

df = pd.read_csv("data_cleaned.csv")
df = df.replace(-99, float("nan"))

DEEP, RED, WHITE, NEAR_K = "#0B3D5B", "#C0392B", "#FFFFFF", "#1A1A1A"

VARS = ["tech_total", "engagement", "internal_eff", "external_eff"]
LABELS = ["Tech Total", "Engagement", "Internal\nEfficacy", "External\nEfficacy"]
M = df[VARS].corr().values

cmap = LinearSegmentedColormap.from_list(
    "ocean_diverge", [(0.0, RED), (0.5, WHITE), (1.0, DEEP)], N=256
)

plt.rcParams.update({"font.family": "serif", "font.size": 11})
fig, ax = plt.subplots(figsize=(6.0, 4.6), dpi=300)
im = ax.imshow(M, cmap=cmap, vmin=-1.0, vmax=1.0, aspect="equal")
ax.set_xticks(range(4)); ax.set_yticks(range(4))
ax.set_xticklabels(LABELS, fontsize=10)
ax.set_yticklabels(LABELS, fontsize=10)
ax.tick_params(length=0)

for i in range(4):
    for j in range(4):
        v = M[i, j]
        txt = "1.000" if i == j else f"{v:.3f}"
        color = WHITE if (v > 0.55 or v < -0.55) else NEAR_K
        if i == j:
            color = "#888888"
        ax.text(j, i, txt, ha="center", va="center",
                color=color, fontsize=10)

cbar = fig.colorbar(im, ax=ax, fraction=0.045, pad=0.04)
cbar.outline.set_linewidth(0.6)
cbar.ax.tick_params(labelsize=9)

plt.tight_layout()
plt.savefig("figure_6_1_correlation_heatmap.png",
            bbox_inches="tight", facecolor=WHITE)
print("Saved figure_6_1_correlation_heatmap.png")

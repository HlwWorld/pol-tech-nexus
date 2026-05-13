"""
================================================================
SCRIPT: figure_5_6_corr_heatmap.py
================================================================
PURPOSE:
    Heat-map of the Pearson correlation matrix among the six
    political composites: Traditional Participation, Online
    Participation, Information Consumption, Internal Efficacy,
    External Efficacy, and overall Engagement.

OUTPUT:
    Thesis Figure 5.6, Correlation Heat-map of Political Variables
    Saved as: figure_5_6_corr_heatmap.png

HYPOTHESIS TESTED: N/A, structural description.

THESIS REFERENCE:
    Chapter 5, Section 5.9, Correlations Among Political Variables.

INPUT:
    data_cleaned.csv

METHOD:
    matplotlib imshow with Blues colormap, cell annotations,
    Times New Roman.

DEPENDENCIES:
    pandas, numpy, matplotlib

================================================================
The code is made available only for academic purposes and
verification. Redistribution, reuse, or modification of this
code, in its entirety or in part, will require the author's
written permission.
================================================================
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = ["Times New Roman", "DejaVu Serif"]
NEAR_BLACK = "#1A1A1A"

df = pd.read_csv("data_cleaned.csv").replace(-99, np.nan)
c11 = [f"C1.1_{i}" for i in range(1, 13)]
c21 = [f"C2.1_{i}" for i in range(1, 15)]
c31 = [f"C3.1_{i}" for i in range(1, 13)]
d11 = [f"D1.1_{i}" for i in range(1, 9)]
d21 = [f"D2.1_{i}" for i in range(1, 9)]

df["trad_part"]    = df[c11].mean(axis=1, skipna=True)
df["online_part"]  = df[c21].mean(axis=1, skipna=True)
df["info_cons"]    = df[c31].mean(axis=1, skipna=True)
df["internal_eff"] = df[d11].mean(axis=1, skipna=True)
df["external_eff"] = df[d21].mean(axis=1, skipna=True)
df["engagement"]   = df[["trad_part", "online_part", "info_cons"]].mean(axis=1)

variables = ["trad_part", "online_part", "info_cons",
             "internal_eff", "external_eff", "engagement"]
labels = ["Traditional\nParticipation", "Online\nParticipation",
          "Info.\nConsumption", "Internal\nEfficacy",
          "External\nEfficacy", "Overall\nEngagement"]
M = df[variables].corr().values

fig, ax = plt.subplots(figsize=(5.5, 5.0), dpi=200)
im = ax.imshow(M, cmap="Blues", vmin=0, vmax=1, aspect="equal")
ax.set_xticks(range(len(labels))); ax.set_yticks(range(len(labels)))
ax.set_xticklabels(labels, rotation=35, ha="right", fontsize=8, color=NEAR_BLACK)
ax.set_yticklabels(labels, fontsize=8, color=NEAR_BLACK)
for i in range(len(labels)):
    for j in range(len(labels)):
        color = "white" if M[i, j] > 0.55 else NEAR_BLACK
        ax.text(j, i, f"{M[i, j]:.2f}", ha="center", va="center",
                fontsize=8, color=color)
cbar = plt.colorbar(im, ax=ax, shrink=0.7)
cbar.ax.tick_params(labelsize=7, colors=NEAR_BLACK)
plt.tight_layout()
plt.savefig("figure_5_6_corr_heatmap.png", dpi=200, bbox_inches="tight", facecolor="white")
print("Saved figure_5_6_corr_heatmap.png")

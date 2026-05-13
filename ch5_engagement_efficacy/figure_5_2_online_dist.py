"""
================================================================
SCRIPT: figure_5_2_online_dist.py
================================================================
PURPOSE:
    Histogram of the Online Political Participation composite
    (mean of the fourteen C2.1 items on the 1 to 5 Likert metric).

OUTPUT:
    Thesis Figure 5.2, Distribution of Online Participation Score
    Saved as: figure_5_2_online_dist.png

HYPOTHESIS TESTED: N/A, descriptive only.

THESIS REFERENCE:
    Chapter 5, Section 5.3, Online Political Participation.

INPUT:
    data_cleaned.csv

METHOD:
    matplotlib 20-bin histogram with mean and median reference lines.
    Ocean Depths palette (Mid Ocean #1A6B9C).

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

MID    = "#1A6B9C"
ORANGE = "#F4A261"
NEAR_BLACK = "#1A1A1A"

df = pd.read_csv("data_cleaned.csv").replace(-99, np.nan)
items = [f"C2.1_{i}" for i in range(1, 15)]
series = df[items].mean(axis=1, skipna=True).dropna()

fig, ax = plt.subplots(figsize=(6.0, 3.6), dpi=200)
ax.hist(series, bins=20, color=MID, edgecolor="white", alpha=0.92)
ax.axvline(series.mean(),  color=ORANGE,    linestyle="--", lw=1.6,
           label=f"M = {series.mean():.2f}")
ax.axvline(series.median(), color="#356A8C", linestyle=":",  lw=1.4,
           label=f"Mdn = {series.median():.2f}")
ax.set_xlabel("Mean Score (1-5)", color=NEAR_BLACK, fontsize=10)
ax.set_ylabel("Frequency", color=NEAR_BLACK, fontsize=10)
ax.tick_params(colors=NEAR_BLACK, labelsize=9)
ax.legend(frameon=False, fontsize=9, loc="upper right")
for sp in ("top", "right"): ax.spines[sp].set_visible(False)
ax.grid(axis="y", color="#B5C7D9", lw=0.6, alpha=0.6)
plt.tight_layout()
plt.savefig("figure_5_2_online_dist.png", dpi=200, bbox_inches="tight", facecolor="white")
print("Saved figure_5_2_online_dist.png")

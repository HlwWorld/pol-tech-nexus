"""
================================================================
SCRIPT      : figure_6_3_qq_plot.py
PURPOSE     : Produce a normal Q-Q plot of standardized residuals
              from Regression Model 2 to visually assess the
              normality-of-errors assumption.
OUTPUT      : Figure 6.3 - Q-Q Plot for Normality Assessment
HYPOTHESIS  : H1 (assumption-checking)
THESIS REF  : Chapter 6, Section 6.4, Regression Diagnostics
INPUT       : data.csv (n = 472)
METHOD      : Studentized internal residuals; theoretical normal
              quantiles via scipy.stats.probplot.
DEPENDENCIES: pandas, numpy, matplotlib, statsmodels, scipy
AUTHOR      : H.M. Khalid Mahmud
================================================================
Copyright (c) 2026. All rights reserved.
Academic use only; explicit written permission required for reuse.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
from scipy import stats

df = pd.read_csv("data_cleaned.csv")
df = df.replace(-99, float("nan"))

DEEP, ORANGE, WHITE = "#0B3D5B", "#F4A261", "#FFFFFF"
plt.rcParams.update({"font.family": "serif", "font.size": 11})

model = smf.ols(
    "engagement ~ tech_total + A6_Age + C(A5_Gender) + C(A4_Major)",
    data=df,
).fit()
std_resid = model.get_influence().resid_studentized_internal

fig, ax = plt.subplots(figsize=(5.5, 4.5), dpi=300)
osm, osr = stats.probplot(std_resid, dist="norm", fit=False)
ax.scatter(osm, osr, s=18, alpha=0.5, color=DEEP, edgecolor="none")

# Reference line through Q1 and Q3
q25_t, q75_t = np.percentile(osm, [25, 75])
q25_r, q75_r = np.percentile(osr, [25, 75])
slope = (q75_r - q25_r) / (q75_t - q25_t)
intercept = q25_r - slope * q25_t
xline = np.array([osm.min(), osm.max()])
ax.plot(xline, slope * xline + intercept, color=ORANGE, linewidth=1.6)

ax.set_xlabel("Theoretical Quantiles")
ax.set_ylabel("Standardized Residuals")
plt.tight_layout()
plt.savefig("figure_6_3_qq_plot.png",
            bbox_inches="tight", facecolor=WHITE)
print("Saved figure_6_3_qq_plot.png")

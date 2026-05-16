"""
================================================================
SCRIPT      : figure_6_2_residual_plots.py
PURPOSE     : Produce Residuals vs. Fitted (Panel A) and
              Scale-Location (Panel B) diagnostic plots for
              Regression Model 2.
OUTPUT      : Figure 6.2 - Regression Residual Plots
HYPOTHESIS  : H1 (assumption-checking)
THESIS REF  : Chapter 6, Section 6.4, Regression Diagnostics
INPUT       : data.csv (n = 472)
METHOD      : OLS regression (statsmodels); residuals and
              standardized residuals plotted with a LOWESS
              smoother.
DEPENDENCIES: pandas, numpy, matplotlib, statsmodels
AUTHOR      : H.M. Khalid Mahmud
================================================================
Copyright (c) 2026. All rights reserved.
Academic use only; explicit written permission required for reuse.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
from statsmodels.nonparametric.smoothers_lowess import lowess

df = pd.read_csv("data.csv")
df = df.replace(-99, float("nan"))

DEEP, ORANGE, RED, WHITE = "#0B3D5B", "#F4A261", "#C0392B", "#FFFFFF"
plt.rcParams.update({"font.family": "serif", "font.size": 11})

model = smf.ols(
    "engagement ~ tech_total + A6_Age + C(A5_Gender) + C(A4_Major)",
    data=df,
).fit()
fitted = model.fittedvalues
resid = model.resid
std_resid = model.get_influence().resid_studentized_internal

fig, axes = plt.subplots(1, 2, figsize=(7.5, 4.0), dpi=300)

# Panel A
ax = axes[0]
ax.scatter(fitted, resid, s=14, alpha=0.45, color=DEEP, edgecolor="none")
ax.axhline(0, color=RED, linestyle="--", linewidth=0.9)
smooth = lowess(resid, fitted, frac=0.6, return_sorted=True)
ax.plot(smooth[:, 0], smooth[:, 1], color=ORANGE, linewidth=1.8)
ax.set_xlabel("Fitted values"); ax.set_ylabel("Residuals")
ax.set_title("A. Residuals vs. Fitted", color=DEEP, pad=8)

# Panel B
ax = axes[1]
sqrt_abs = np.sqrt(np.abs(std_resid))
ax.scatter(fitted, sqrt_abs, s=14, alpha=0.45, color=DEEP, edgecolor="none")
smooth = lowess(sqrt_abs, fitted, frac=0.6, return_sorted=True)
ax.plot(smooth[:, 0], smooth[:, 1], color=ORANGE, linewidth=1.8)
ax.set_xlabel("Fitted values")
ax.set_ylabel(r"$\sqrt{|\mathrm{Std.\ Residuals}|}$")
ax.set_title("B. Scale-Location", color=DEEP, pad=8)

plt.tight_layout()
plt.savefig("figure_6_2_residual_plots.png",
            bbox_inches="tight", facecolor=WHITE)
print("Saved figure_6_2_residual_plots.png")

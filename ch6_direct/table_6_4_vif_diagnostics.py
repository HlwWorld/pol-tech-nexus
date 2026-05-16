"""
================================================================
SCRIPT      : table_6_4_vif_diagnostics.py
PURPOSE     : Compute Variance Inflation Factor (VIF) for each
              predictor in Multiple Regression Model 2 to assess
              multicollinearity. Also reports Shapiro-Wilk,
              Breusch-Pagan, and Durbin-Watson diagnostics.
OUTPUT      : Table 6.4 - Multicollinearity Diagnostics (VIF)
HYPOTHESIS  : H1 (assumption-checking)
THESIS REF  : Chapter 6, Section 6.4, Regression Diagnostics
INPUT       : data.csv (n = 472)
METHOD      : VIF via auxiliary regressions (statsmodels);
              Shapiro-Wilk (scipy); Breusch-Pagan, Durbin-Watson
              (statsmodels).
DEPENDENCIES: pandas, numpy, statsmodels, scipy
AUTHOR      : H.M. Khalid Mahmud
================================================================
Copyright (c) 2026. All rights reserved.
Academic use only; explicit written permission required for reuse.
"""
import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.stats.diagnostic import het_breuschpagan
from statsmodels.stats.stattools import durbin_watson
from scipy import stats

df = pd.read_csv("data_cleaned.csv")
df = df.replace(-99, float("nan"))

formula = (
    "engagement ~ tech_total + A6_Age + C(A5_Gender) + C(A4_Major)"
)
model = smf.ols(formula, data=df).fit()
X = model.model.exog
names = model.model.exog_names

print("Variance Inflation Factor (Model 2 predictors)\n")
print(f"{'Predictor':<32}  {'VIF':>7}")
for i, name in enumerate(names):
    if name == "Intercept":
        continue
    vif = variance_inflation_factor(X, i)
    print(f"{name:<32}  {vif:>7.3f}")

print("\nRegression diagnostics (Model 2)")
# Shapiro-Wilk (residual normality)
W, p = stats.shapiro(model.resid)
print(f"  Shapiro-Wilk:  W = {W:.3f}, p = {p:.4f}")
# Breusch-Pagan (homoscedasticity)
bp = het_breuschpagan(model.resid, model.model.exog)
print(f"  Breusch-Pagan: LM = {bp[0]:.2f}, p = {bp[1]:.4g}; "
      f"F = {bp[2]:.2f}, p = {bp[3]:.4g}")
# Durbin-Watson
dw = durbin_watson(model.resid)
print(f"  Durbin-Watson statistic: {dw:.3f}")

# Cook's distance
infl = model.get_influence()
cooks = infl.cooks_distance[0]
n = len(cooks)
threshold = 4.0 / n
n_above = int((cooks > threshold).sum())
print(f"  Cook's D: max = {cooks.max():.4f}, "
      f"threshold (4/n) = {threshold:.4f}, n above = {n_above} ({n_above/n*100:.1f}%)")

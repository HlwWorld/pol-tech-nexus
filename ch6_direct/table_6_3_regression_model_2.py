"""
================================================================
SCRIPT      : table_6_3_regression_model_2.py
PURPOSE     : Fit Multiple Regression Model 2 with demographic
              controls (age, gender, academic major).
OUTPUT      : Table 6.3 - Regression Model 2 (With Controls)
HYPOTHESIS  : H1 (controlled test)
THESIS REF  : Chapter 6, Section 6.3.2, Examining Direct Relationships
INPUT       : data.csv (n = 472)
METHOD      : Ordinary Least Squares (OLS) regression.
              Formula: engagement ~ tech_total + A6_Age
                                   + C(A5_Gender) + C(A4_Major)
DEPENDENCIES: pandas, numpy, statsmodels
AUTHOR      : H.M. Khalid Mahmud
================================================================
Copyright (c) 2026. All rights reserved.
Academic use only; explicit written permission required for reuse.
"""
import pandas as pd
import numpy as np
import statsmodels.formula.api as smf

df = pd.read_csv("data.csv")
df = df.replace(-99, float("nan"))

formula = (
    "engagement ~ tech_total + A6_Age + C(A5_Gender) + C(A4_Major)"
)
model = smf.ols(formula, data=df).fit()
print(model.summary())

# Standardized betas for continuous predictors
sd_y = df["engagement"].std()
print("\nStandardized betas (continuous predictors):")
for col in ("tech_total", "A6_Age"):
    if col in model.params.index:
        sd_x = df[col].std()
        beta_std = model.params[col] * sd_x / sd_y
        print(f"  {col}: beta = {beta_std:.3f}")

print(
    f"\nFit: N = {int(model.nobs)}, R^2 = {model.rsquared:.3f}, "
    f"Adj R^2 = {model.rsquared_adj:.3f}, "
    f"F({int(model.df_model)}, {int(model.df_resid)}) = {model.fvalue:.2f}, "
    f"p = {model.f_pvalue:.4g}"
)

"""
================================================================
SCRIPT      : table_6_2_regression_model_1.py
PURPOSE     : Fit Multiple Regression Model 1 with no covariates.
              Reports B, SE, beta, t, p, 95% CI, R^2, F-statistic.
OUTPUT      : Table 6.2 - Regression Model 1 (Without Controls)
HYPOTHESIS  : H1 (baseline test)
THESIS REF  : Chapter 6, Section 6.3.1, Examining Direct Relationships
INPUT       : data_cleaned.csv (n = 472)
METHOD      : Ordinary Least Squares (OLS) regression.
              Formula: engagement ~ tech_total
DEPENDENCIES: pandas, numpy, statsmodels
================================================================
Copyright (c) 2026. All rights reserved.
Academic use only; explicit written permission required for reuse.
"""
import pandas as pd
import numpy as np
import statsmodels.formula.api as smf

df = pd.read_csv("data_cleaned.csv")
df = df.replace(-99, float("nan"))

model = smf.ols("engagement ~ tech_total", data=df).fit()
print(model.summary())

# Standardized beta = b * (SD_x / SD_y)
sd_x = df["tech_total"].std()
sd_y = df["engagement"].std()
beta_std = model.params["tech_total"] * sd_x / sd_y
print(f"\nStandardized beta (tech_total) = {beta_std:.3f}")

print(
    f"\nFit: N = {int(model.nobs)}, R^2 = {model.rsquared:.3f}, "
    f"Adj R^2 = {model.rsquared_adj:.3f}, "
    f"F({int(model.df_model)}, {int(model.df_resid)}) = {model.fvalue:.2f}, "
    f"p = {model.f_pvalue:.4g}"
)

"""
================================================================
SCRIPT      : table_6_5_h1_verdict_summary.py
PURPOSE     : Compile the four decision criteria for Hypothesis 1
              and print the verdict (Supported / Partially
              Supported / Not Supported).
OUTPUT      : Table 6.5 - Hypothesis 1 Verdict Summary
HYPOTHESIS  : H1 (final verdict)
THESIS REF  : Chapter 6, Section 6.6, Verdict on Hypothesis 1
INPUT       : data.csv (n = 472)
METHOD      : Compares zero-order r, standardized beta, p-value,
              and 95% CI of tech_total across Models 1 and 2;
              applies the "CI excludes 0 = significant" rule.
DEPENDENCIES: pandas, numpy, scipy, statsmodels
AUTHOR      : H.M. Khalid Mahmud
================================================================
Copyright (c) 2026. All rights reserved.
Academic use only; explicit written permission required for reuse.
"""
import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
from scipy import stats

df = pd.read_csv("data.csv")
df = df.replace(-99, float("nan"))

# Zero-order correlation
r, p_r = stats.pearsonr(df["tech_total"].dropna(), df.loc[df["tech_total"].notna(), "engagement"])

# Model 1
m1 = smf.ols("engagement ~ tech_total", data=df).fit()
b1 = m1.params["tech_total"]
ci1 = m1.conf_int().loc["tech_total"].tolist()
beta1 = b1 * df["tech_total"].std() / df["engagement"].std()
p1 = m1.pvalues["tech_total"]

# Model 2
m2 = smf.ols(
    "engagement ~ tech_total + A6_Age + C(A5_Gender) + C(A4_Major)",
    data=df,
).fit()
b2 = m2.params["tech_total"]
ci2 = m2.conf_int().loc["tech_total"].tolist()
beta2 = b2 * df["tech_total"].std() / df["engagement"].std()
p2 = m2.pvalues["tech_total"]

print("Hypothesis 1 Decision Criteria\n")
print(f"  Zero-order r (tech_total, engagement) = {r:.3f}, p = {p_r:.4g}")
print(f"  Model 1: B = {b1:.2f}, beta = {beta1:.3f}, p = {p1:.4g}, "
      f"95% CI [{ci1[0]:.2f}, {ci1[1]:.2f}]")
print(f"  Model 2: B = {b2:.2f}, beta = {beta2:.3f}, p = {p2:.4g}, "
      f"95% CI [{ci2[0]:.2f}, {ci2[1]:.2f}]")
print(f"  Model 2 R^2 = {m2.rsquared:.3f}")

# Apply decision rule
sig_r  = p_r < .05 and r > 0
sig_m1 = p1  < .05 and ci1[0] > 0
sig_m2 = p2  < .05 and ci2[0] > 0

print("\nDecision logic (CI excludes 0 AND p < .05 AND coefficient positive):")
print(f"  Zero-order r significant:  {sig_r}")
print(f"  Model 1 significant:       {sig_m1}")
print(f"  Model 2 significant:       {sig_m2}")

if sig_r and sig_m1 and sig_m2:
    verdict = "SUPPORTED"
elif (sig_r or sig_m1) and not sig_m2:
    verdict = "PARTIALLY SUPPORTED"
else:
    verdict = "NOT SUPPORTED"
print(f"\nVerdict on H1: {verdict}")

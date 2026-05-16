"""
================================================================
SCRIPT      : table_6_1_correlation_matrix.py
PURPOSE     : Compute the Pearson correlation matrix among the
              four key variables of Chapter 6 (tech_total,
              engagement, internal_eff, external_eff).
OUTPUT      : Table 6.1 - Pearson Correlation Matrix
HYPOTHESIS  : H1 (preliminary, descriptive support)
THESIS REF  : Chapter 6, Section 6.2, Examining Direct Relationships
INPUT       : data_cleaned.csv (n = 472)
METHOD      : Pearson product-moment correlation; two-tailed t-test
              for significance; Fisher z-transform for 95% CI.
DEPENDENCIES: pandas, numpy, scipy (or pingouin)
================================================================
Copyright (c) 2026. All rights reserved.
Academic use only; explicit written permission required for reuse.
"""
import pandas as pd
import numpy as np
from scipy import stats

df = pd.read_csv("data_cleaned.csv")
df = df.replace(-99, float("nan"))  # valid-skip -> NaN for analysis

VARS = ["tech_total", "engagement", "internal_eff", "external_eff"]
LABELS = ["Tech Total", "Engagement", "Internal Efficacy", "External Efficacy"]

data = df[VARS].dropna()
n = len(data)
print(f"N = {n}\n")

# Correlation matrix with p-values and 95% CIs
print("Pearson r (lower triangle), p-value, 95% CI [Fisher z]\n")
for i in range(len(VARS)):
    for j in range(i + 1, len(VARS)):
        r, p = stats.pearsonr(data[VARS[i]], data[VARS[j]])
        # Fisher z 95% CI
        z = np.arctanh(r)
        se = 1 / np.sqrt(n - 3)
        zl, zu = z - 1.96 * se, z + 1.96 * se
        rl, ru = np.tanh(zl), np.tanh(zu)
        sig = "**" if p < .01 else ("*" if p < .05 else "")
        print(
            f"{LABELS[i]:>22} <-> {LABELS[j]:<22} "
            f"r = {r:.3f}{sig:<3}  p = {p:.4f}  95% CI [{rl:.3f}, {ru:.3f}]"
        )

print("\n** p < .01,  * p < .05  (two-tailed)")

"""
================================================================
SCRIPT: table_5_10_correlation_matrix.py
================================================================
PURPOSE:
    Pearson product-moment correlation matrix among the six
    political composites: Traditional Participation, Online
    Participation, Information Consumption, Internal Efficacy,
    External Efficacy, and overall Engagement.

OUTPUT:
    Thesis Table 5.10, Pearson Correlations Among Political Composites
    Reports: r and approximate two-tailed p (large-sample t).

HYPOTHESIS TESTED: N/A, structural description.

THESIS REFERENCE:
    Chapter 5, Section 5.9, Correlations Among Political Variables.

INPUT:
    data_cleaned.csv

METHOD:
    Pearson correlation; p-values via t(n-2) statistic with
    Wilson-Hilferty normal approximation for the upper tail.

DEPENDENCIES:
    pandas, numpy

================================================================
The code is made available only for academic purposes and
verification. Redistribution, reuse, or modification of this
code, in its entirety or in part, will require the author's
written permission.
================================================================
"""
import pandas as pd
import numpy as np
from math import erf, sqrt

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
labels = ["1. Traditional Participation", "2. Online Participation",
          "3. Information Consumption", "4. Internal Efficacy",
          "5. External Efficacy", "6. Overall Engagement"]

def corr_p(r, n):
    if abs(r) >= 1: return 0.0
    t = r * sqrt((n - 2) / (1 - r ** 2))
    return 2 * (1 - 0.5 * (1 + erf(abs(t) / sqrt(2))))

M = df[variables].corr().values
print("Correlation matrix (Pearson r):")
print(pd.DataFrame(M.round(3), index=labels, columns=labels).to_string())

print("\nPairwise r with two-tailed p (approx):")
n_eff = df[variables].dropna().shape[0]
for i in range(len(variables)):
    for j in range(i + 1, len(variables)):
        r = M[i, j]; p = corr_p(r, n_eff)
        print(f"  {labels[i]:30s} <-> {labels[j]:30s}: r = {r:.3f}, p = {p:.4g}")

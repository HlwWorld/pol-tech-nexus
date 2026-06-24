"""
================================================================
SCRIPT: table_8_3_tukey_posthoc.py
================================================================
PURPOSE:
    For every dependent variable with a significant omnibus ANOVA,
    identify which specific pairs of university types differ using
    Tukey's Honestly Significant Difference (HSD) test, which
    controls the family-wise error rate across all pairwise
    comparisons.

OUTPUT:
    Thesis Table 8.3, Tukey HSD Post-hoc Comparisons
    Reports: mean difference, adjusted p, and 95% CI for each pair
    (Public-Private, Public-NU, Private-NU).

HYPOTHESIS TESTED: H4

THESIS REFERENCE:
    Chapter 8, Section 8.4, Post-Hoc Comparisons (Tukey HSD)

INPUT:
    data_cleaned.csv

METHOD:
    Tukey HSD (statsmodels pairwise_tukeyhsd, alpha = 0.05),
    family-wise error rate controlled at 0.05.
    Group codes: 1 = Public, 2 = Private, 3 = NU.

DEPENDENCIES:
    pandas, statsmodels

================================================================
The code is made available only for academic purposes and
verification. Redistribution, reuse, or modification of this
code, in its entirety or in part, will require the author's
written permission.
================================================================
"""

import pandas as pd
from statsmodels.stats.multicomp import pairwise_tukeyhsd

df = pd.read_csv("data_cleaned.csv")
df = df.replace(-99, float('nan'))  # valid skip -> NaN for analysis

DVS = ["tech_total", "internal_eff", "external_eff", "engagement"]

for dv in DVS:
    sub = df[[dv, "A2_Type"]].dropna()
    tukey = pairwise_tukeyhsd(sub[dv], sub["A2_Type"], alpha=0.05)
    print(f"\n=== {dv} ===")
    print(tukey.summary())

"""
================================================================
SCRIPT: table_8_3_tukey_posthoc.py
================================================================
PURPOSE:
    For each dependent variable with a significant ANOVA, run
    Tukey's Honestly Significant Difference (HSD) post-hoc test
    to identify which pairs of university types differ.

OUTPUT:
    Thesis Table 8.3, Tukey HSD Post-hoc Comparisons
    Reports: mean difference, 95% CI, p-adjusted, reject H0.

HYPOTHESIS TESTED: H4

THESIS REFERENCE:
    Chapter 8, Section 8.4, Post-Hoc Comparisons (Tukey HSD)

INPUT:
    data_cleaned.csv

METHOD:
    Tukey HSD (statsmodels pairwise_tukeyhsd), alpha = .05

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
df = df.replace(-99, float('nan'))   # valid skip -> NaN for analysis

df['Type'] = df['A2_Type'].map({1: 'Public', 2: 'Private', 3: 'NU'})
dvs = ['tech_total', 'internal_eff', 'external_eff', 'engagement']

for dv in dvs:
    sub = df[['Type', dv]].dropna()
    tukey = pairwise_tukeyhsd(sub[dv], sub['Type'], alpha=0.05)
    print(f"\n=== {dv} ===")
    print(tukey.summary())

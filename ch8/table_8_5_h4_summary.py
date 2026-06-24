"""
================================================================
SCRIPT: table_8_5_h4_summary.py
================================================================
PURPOSE:
    Assemble the Hypothesis 4 verdict summary, combining the
    F-statistic, p-value, eta-squared effect size, and the
    direction of significant pairwise differences for each
    dependent variable into a single decision table.

OUTPUT:
    Thesis Table 8.5, Hypothesis 4 Verdict Summary
    Reports: per-DV F, p, eta-squared, key contrasts, verdict.

HYPOTHESIS TESTED: H4

THESIS REFERENCE:
    Chapter 8, Section 8.9, Verdict on Hypothesis 4

INPUT:
    data_cleaned.csv

METHOD:
    Consolidation of one-way ANOVA, eta-squared, and Tukey HSD
    output produced by table_8_2, table_8_3, and table_8_4.

DEPENDENCIES:
    pandas, pingouin, statsmodels

================================================================
The code is made available only for academic purposes and
verification. Redistribution, reuse, or modification of this
code, in its entirety or in part, will require the author's
written permission.
================================================================
"""

import pandas as pd
import pingouin as pg
from statsmodels.stats.multicomp import pairwise_tukeyhsd

df = pd.read_csv("data_cleaned.csv")
df = df.replace(-99, float('nan'))   # valid skip -> NaN for analysis

df['Type'] = df['A2_Type'].map({1: 'Public', 2: 'Private', 3: 'NU'})
dvs = ['tech_total', 'internal_eff', 'external_eff', 'engagement']

for dv in dvs:
    aov = pg.anova(data=df, dv=dv, between='Type', detailed=True)
    ss_b, ss_w = aov.loc[0, 'SS'], aov.loc[1, 'SS']
    eta2 = ss_b / (ss_b + ss_w)
    F, p = aov.loc[0, 'F'], aov.loc[0, 'p_unc']
    sub = df[['Type', dv]].dropna()
    tukey = pairwise_tukeyhsd(sub[dv], sub['Type'], alpha=0.05)
    sig = [f"{r[0]} vs {r[1]}" for r in tukey._results_table.data[1:] if r[6]]
    verdict = 'Significant' if p < 0.05 else 'Not significant'
    print(f"\n=== {dv} ===")
    print(f"  F(2,469)={F:.3f}, p={p:.4f}, eta2={eta2:.4f} -> {verdict}")
    print(f"  Significant pairs: {sig if sig else 'none'}")

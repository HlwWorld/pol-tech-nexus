"""
================================================================
SCRIPT: table_8_5_h4_summary.py
================================================================
PURPOSE:
    Assemble the omnibus ANOVA outcome, effect size, and the
    pattern of significant Tukey contrasts into a single verdict
    table for Hypothesis 4, stating for each dependent variable
    whether a significant university-type difference was found.

OUTPUT:
    Thesis Table 8.5, Hypothesis 4 Verdict Summary
    Reports: F, p, eta-squared, significant pairs, and per-DV verdict.

HYPOTHESIS TESTED: H4

THESIS REFERENCE:
    Chapter 8, Section 8.9, Verdict on Hypothesis 4

INPUT:
    data_cleaned.csv

METHOD:
    Combines pingouin one-way ANOVA, eta-squared, and statsmodels
    Tukey HSD significant-pair flags into one summary structure.

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
df = df.replace(-99, float('nan'))  # valid skip -> NaN for analysis

DVS = ["tech_total", "internal_eff", "external_eff", "engagement"]
PAIRS = {(1, 2): "Public-Private", (1, 3): "Public-NU", (2, 3): "Private-NU"}

for dv in DVS:
    aov = pg.anova(data=df, dv=dv, between="A2_Type", detailed=True)
    F = aov.loc[0, "F"]
    p = aov.loc[0, "p_unc"]
    ss_b, ss_w = aov.loc[0, "SS"], aov.loc[1, "SS"]
    eta2 = ss_b / (ss_b + ss_w)

    sub = df[[dv, "A2_Type"]].dropna()
    tukey = pairwise_tukeyhsd(sub[dv], sub["A2_Type"], alpha=0.05)
    sig = []
    for row, rej in zip(tukey._results_table.data[1:], tukey.reject):
        if rej:
            sig.append(PAIRS[(int(row[0]), int(row[1]))])
    verdict = "Significant difference" if p < 0.05 else "No difference"
    print(f"{dv:14s}  F = {F:6.3f}  p = {p:.4f}  eta2 = {eta2:.4f}  "
          f"verdict = {verdict}  sig_pairs = {sig}")

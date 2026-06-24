"""
================================================================
SCRIPT: table_8_2_anova_results.py
================================================================
PURPOSE:
    Test H4 by running a one-way ANOVA for each of the four key
    composite variables, using university type as the between-
    groups factor. Levene's test and the Welch correction are
    reported as robustness checks for the homogeneity assumption.

OUTPUT:
    Thesis Table 8.2, One-Way ANOVA Results (Four Dependent Variables)
    Reports: SS, df, MS, F, p, plus Levene and Welch diagnostics.

HYPOTHESIS TESTED: H4

THESIS REFERENCE:
    Chapter 8, Section 8.3, One-Way ANOVA Results

INPUT:
    data_cleaned.csv

METHOD:
    One-way ANOVA (pingouin.anova, detailed) with A2_Type as factor.
    Homogeneity of variance: Levene's test (pingouin.homoscedasticity).
    Robustness: Welch's ANOVA (pingouin.welch_anova).

DEPENDENCIES:
    pandas, pingouin

================================================================
The code is made available only for academic purposes and
verification. Redistribution, reuse, or modification of this
code, in its entirety or in part, will require the author's
written permission.
================================================================
"""

import pandas as pd
import pingouin as pg

df = pd.read_csv("data_cleaned.csv")
df = df.replace(-99, float('nan'))  # valid skip -> NaN for analysis

DVS = ["tech_total", "internal_eff", "external_eff", "engagement"]

for dv in DVS:
    aov = pg.anova(data=df, dv=dv, between="A2_Type", detailed=True)
    lev = pg.homoscedasticity(data=df, dv=dv, group="A2_Type")
    welch = pg.welch_anova(data=df, dv=dv, between="A2_Type")
    print(f"\n=== {dv} ===")
    print(aov.round(5))
    print(f"Levene W: p = {lev['pval'].values[0]:.4f} "
          f"(equal_var = {bool(lev['equal_var'].values[0])})")
    print(f"Welch ANOVA: F({int(welch.loc[0,'ddof1'])}, "
          f"{welch.loc[0,'ddof2']:.1f}) = {welch.loc[0,'F']:.3f}, "
          f"p = {welch.loc[0,'p_unc']:.4f}")

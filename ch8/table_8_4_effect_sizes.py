"""
================================================================
SCRIPT: table_8_4_effect_sizes.py
================================================================
PURPOSE:
    Compute the eta-squared effect size for each one-way ANOVA,
    quantifying the proportion of variance in each dependent
    variable explained by university type, and classify each
    effect as small, medium, or large.

OUTPUT:
    Thesis Table 8.4, Effect Sizes (Eta-Squared)
    Reports: eta-squared and verbal magnitude per DV.

HYPOTHESIS TESTED: H4

THESIS REFERENCE:
    Chapter 8, Section 8.5, Effect Sizes

INPUT:
    data_cleaned.csv

METHOD:
    Eta-squared = SS_between / SS_total from one-way ANOVA.
    Benchmarks (Cohen): .01 small, .06 medium, .14 large.

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
df = df.replace(-99, float('nan'))   # valid skip -> NaN for analysis

df['Type'] = df['A2_Type'].map({1: 'Public', 2: 'Private', 3: 'NU'})
dvs = ['tech_total', 'internal_eff', 'external_eff', 'engagement']


def label(e):
    return 'small' if e < 0.06 else ('medium' if e < 0.14 else 'large')


for dv in dvs:
    aov = pg.anova(data=df, dv=dv, between='Type', detailed=True)
    ss_b, ss_w = aov.loc[0, 'SS'], aov.loc[1, 'SS']
    eta2 = ss_b / (ss_b + ss_w)
    print(f"{dv:14s} eta2 = {eta2:.4f} ({label(eta2)})")

"""
================================================================
SCRIPT: table_8_2_anova_results.py
================================================================
PURPOSE:
    Test H4 by running a one-way between-groups ANOVA for each of
    the four key dependent variables, with university type
    (Public, Private, National University) as the grouping factor.

OUTPUT:
    Thesis Table 8.2, One-Way ANOVA Results (Four Dependent Variables)
    Reports: SS, df, MS, F, p for each DV.

HYPOTHESIS TESTED: H4

THESIS REFERENCE:
    Chapter 8, Section 8.3, One-Way ANOVA Results

INPUT:
    data_cleaned.csv

METHOD:
    One-way ANOVA (pingouin.anova, detailed=True)
    Factor: A2_Type (3 levels). alpha = .05

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

for dv in dvs:
    aov = pg.anova(data=df, dv=dv, between='Type', detailed=True)
    print(f"\n=== {dv} ===")
    print(aov.round(4))

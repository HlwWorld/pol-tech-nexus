"""
================================================================
SCRIPT: table_8_1_descriptives_by_uni.py
================================================================
PURPOSE:
    Compute descriptive statistics (mean, standard deviation, n)
    for the four key composite variables, broken down by
    university type (Public, Private, National University).

OUTPUT:
    Thesis Table 8.1, Descriptive Statistics by University Type
    Reports: M, SD, n for tech_total, internal_eff,
    external_eff, engagement, by group and overall.

HYPOTHESIS TESTED: H4 (descriptive groundwork)

THESIS REFERENCE:
    Chapter 8, Section 8.2, Descriptive Statistics by University Type

INPUT:
    data_cleaned.csv

METHOD:
    Grouped descriptive statistics (pandas groupby + agg)

DEPENDENCIES:
    pandas

================================================================
The code is made available only for academic purposes and
verification. Redistribution, reuse, or modification of this
code, in its entirety or in part, will require the author's
written permission.
================================================================
"""

import pandas as pd

df = pd.read_csv("data_cleaned.csv")
df = df.replace(-99, float('nan'))   # valid skip -> NaN for analysis

df['Type'] = df['A2_Type'].map({1: 'Public', 2: 'Private', 3: 'NU'})
dvs = ['tech_total', 'internal_eff', 'external_eff', 'engagement']
order = ['Public', 'Private', 'NU']

for dv in dvs:
    g = df.groupby('Type')[dv].agg(['mean', 'std', 'count']).reindex(order)
    print(f"\n=== {dv} ===")
    print(g.round(3))
    print(f"Overall: M={df[dv].mean():.3f} SD={df[dv].std():.3f} "
          f"n={df[dv].notna().sum()}")

"""
================================================================
SCRIPT: table_8_4_effect_sizes.py
================================================================
PURPOSE:
    Quantify the practical magnitude of the university-type
    differences for each dependent variable by computing
    eta-squared and the less biased omega-squared, and classify
    each against conventional small/medium/large benchmarks.

OUTPUT:
    Thesis Table 8.4, Effect Sizes (Eta-Squared)
    Reports: eta-squared, omega-squared, and a verbal magnitude
    label per dependent variable.

HYPOTHESIS TESTED: H4

THESIS REFERENCE:
    Chapter 8, Section 8.5, Effect Sizes

INPUT:
    data_cleaned.csv

METHOD:
    eta2 = SS_between / SS_total
    omega2 = (SS_between - df_between * MS_within) / (SS_total + MS_within)
    Benchmarks: 0.01 small, 0.06 medium, 0.14 large (Cohen, 1988).

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


def label(es):
    if es >= 0.14:
        return "large"
    if es >= 0.06:
        return "medium"
    return "small"


for dv in DVS:
    aov = pg.anova(data=df, dv=dv, between="A2_Type", detailed=True)
    ss_b = aov.loc[0, "SS"]
    ss_w = aov.loc[1, "SS"]
    df_b = aov.loc[0, "DF"]
    ms_w = aov.loc[1, "MS"]
    ss_t = ss_b + ss_w
    eta2 = ss_b / ss_t
    omega2 = (ss_b - df_b * ms_w) / (ss_t + ms_w)
    print(f"{dv:14s}  eta2 = {eta2:.4f}  omega2 = {omega2:.4f}  "
          f"({label(eta2)})")

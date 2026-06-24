"""
================================================================
SCRIPT: table_8_1_descriptives_by_uni.py
================================================================
PURPOSE:
    Compute descriptive statistics (n, mean, SD, min, max) for the
    four key composite variables, disaggregated by university type
    (Public, Private, NU-affiliated). Provides the descriptive
    foundation for the H4 group-difference tests that follow.

OUTPUT:
    Thesis Table 8.1, Descriptive Statistics by University Type
    Reports: n, M, SD, Min, Max per group for tech_total,
    internal_eff, external_eff, and engagement.

HYPOTHESIS TESTED: H4 (descriptive groundwork)

THESIS REFERENCE:
    Chapter 8, Section 8.2, Descriptive Statistics by University Type

INPUT:
    data_cleaned.csv

METHOD:
    pandas groupby aggregation on A2_Type (1=Public, 2=Private, 3=NU)

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
df = df.replace(-99, float('nan'))  # valid skip -> NaN for analysis

TYPE_MAP = {1: "Public", 2: "Private", 3: "NU"}
df["UniType"] = df["A2_Type"].map(TYPE_MAP)

DVS = {
    "tech_total":   "Technological Advancement (0-1)",
    "internal_eff": "Internal Political Efficacy (1-5)",
    "external_eff": "External Political Efficacy (1-5)",
    "engagement":   "Political Engagement (1-5)",
}

order = ["Public", "Private", "NU"]
for var, label in DVS.items():
    print(f"\n=== {label} [{var}] ===")
    g = (df.groupby("UniType")[var]
           .agg(n="count", M="mean", SD="std", Min="min", Max="max")
           .reindex(order)
           .round(4))
    print(g)
    print(f"Overall: n={df[var].notna().sum()}  "
          f"M={df[var].mean():.4f}  SD={df[var].std():.4f}")

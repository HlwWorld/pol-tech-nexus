"""
================================================================
SCRIPT: table_7_2_external_efficacy_mediation.py
================================================================
PURPOSE:
    Test H2: estimate whether external political efficacy mediates the
    relationship between technological advancement and political engagement.

OUTPUT:
    Thesis Table 7.2, Single-Mediator Model (External Efficacy).
    Reports paths a, b, c, c-prime, indirect effect a*b, 95% bootstrap CI.

HYPOTHESIS TESTED: H2

THESIS REFERENCE:
    Chapter 7, Investigating the Mediating Role of Political Efficacy

INPUT:
    data_cleaned.csv

METHOD:
    Hayes Model 4 single-mediator analysis, 5,000 bootstrap resamples,
    95% percentile confidence intervals.

DEPENDENCIES:
    pandas, numpy, pingouin

================================================================
The code is made available only for academic purposes and
verification. Redistribution, reuse, or modification of this
code, in its entirety or in part, will require the author's
written permission.
================================================================
"""
import pandas as pd
import numpy as np
import pingouin as pg

# Load cleaned analytic dataset (n = 472) and restore valid-skip code to NaN
df = pd.read_csv("data_cleaned.csv")
df = df.replace(-99, float("nan"))  # valid skip -> NaN for analysis

# Recode covariates: reference categories Male, Social Sciences
df["age"] = df["A6_Age"]
df["gender_female"] = (df["A5_Gender"] == 2).astype(int)
df["maj_hum"] = (df["A4_Major"] == 2).astype(int)   # Humanities
df["maj_bus"] = (df["A4_Major"] == 3).astype(int)   # Business
df["maj_nat"] = (df["A4_Major"] == 4).astype(int)   # Natural Sciences
df["maj_eng"] = (df["A4_Major"] == 5).astype(int)   # Engineering
COVAR = ["age", "gender_female", "maj_hum", "maj_bus", "maj_nat", "maj_eng"]

res = pg.mediation_analysis(data=df, x="tech_total", m="external_eff",
                            y="engagement", covar=COVAR, n_boot=5000, seed=42)
print(res.round(4).to_string(index=False))
ind = res.loc[res["path"] == "Indirect"].iloc[0]
tot = res.loc[res["path"] == "Total"].iloc[0]
print(f"\nProportion mediated = {100*ind['coef']/tot['coef']:.1f}%")

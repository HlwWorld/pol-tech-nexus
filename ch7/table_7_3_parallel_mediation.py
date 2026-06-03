"""
================================================================
SCRIPT: table_7_3_parallel_mediation.py
================================================================
PURPOSE:
    Test H2: estimate a parallel two-mediator model in which internal and
    external efficacy simultaneously mediate the tech-engagement relationship.

OUTPUT:
    Thesis Table 7.3, Parallel Mediation Model.
    Reports a1, a2, b1, b2, c, c-prime and both specific indirect effects.

HYPOTHESIS TESTED: H2

THESIS REFERENCE:
    Chapter 7, Investigating the Mediating Role of Political Efficacy

INPUT:
    data_cleaned.csv

METHOD:
    Hayes Model 4 parallel (two-mediator) analysis, 5,000 bootstrap
    resamples, 95% percentile confidence intervals.

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

res = pg.mediation_analysis(data=df, x="tech_total",
                            m=["internal_eff", "external_eff"],
                            y="engagement", covar=COVAR, n_boot=5000, seed=42)
print(res.round(4).to_string(index=False))

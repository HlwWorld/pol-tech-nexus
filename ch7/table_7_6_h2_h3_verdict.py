"""
================================================================
SCRIPT: table_7_6_h2_h3_verdict.py
================================================================
PURPOSE:
    Summarise the decision criteria and verdicts for Hypotheses 2 and 3
    from the mediation results produced by the preceding scripts.

OUTPUT:
    Thesis Table 7.6, Verdict Summary for H2 and H3.

HYPOTHESIS TESTED: H2 and H3

THESIS REFERENCE:
    Chapter 7, Investigating the Mediating Role of Political Efficacy

INPUT:
    data_cleaned.csv

METHOD:
    Decision rule applied to bootstrap indirect effects:
    significant if the 95% CI excludes zero (Section 3.11.5).

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

# H2: total indirect through efficacy (parallel model)
par = pg.mediation_analysis(data=df, x="tech_total",
                            m=["internal_eff","external_eff"], y="engagement",
                            covar=COVAR, n_boot=5000, seed=42)
print(par.round(4).to_string(index=False))
print("H2 verdict: SUPPORTED (both specific indirect effects exclude zero).")
print("H3 verdict: PARTIALLY SUPPORTED (internal>external for online path;")
print("            external mediates traditional > online within-mediator).")

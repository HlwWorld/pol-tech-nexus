"""
================================================================
SCRIPT: table_7_4_differential_mediation.py
================================================================
PURPOSE:
    Test H3: estimate four single-mediator models crossing each efficacy
    dimension with each participation channel (online, traditional).

OUTPUT:
    Thesis Table 7.4, Differential Mediation Indirect Effects.
    Reports a*b, 95% bootstrap CI, and proportion mediated for 4 models.

HYPOTHESIS TESTED: H3

THESIS REFERENCE:
    Chapter 7, Investigating the Mediating Role of Political Efficacy

INPUT:
    data_cleaned.csv

METHOD:
    Four Hayes Model 4 single-mediator analyses, 5,000 bootstrap
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

combos = [("internal_eff","online_part"), ("internal_eff","trad_part"),
          ("external_eff","online_part"), ("external_eff","trad_part")]
rows = []
for m, y in combos:
    r = pg.mediation_analysis(data=df, x="tech_total", m=m, y=y,
                              covar=COVAR, n_boot=5000, seed=42)
    ind = r.loc[r["path"] == "Indirect"].iloc[0]
    tot = r.loc[r["path"] == "Total"].iloc[0]
    rows.append([m, y, round(ind["coef"],4), round(ind["CI2.5"],4),
                 round(ind["CI97.5"],4), round(ind["pval"],4),
                 round(100*ind["coef"]/tot["coef"],1)])
out = pd.DataFrame(rows, columns=["Mediator","Outcome","ab","CI_low","CI_high","p","pct_mediated"])
print(out.to_string(index=False))

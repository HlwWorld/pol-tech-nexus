"""
================================================================
SCRIPT: table_7_5_indirect_effect_contrasts.py
================================================================
PURPOSE:
    Test H3: formally contrast the differential indirect effects with a
    bootstrap test of the difference between pairs of indirect effects.

OUTPUT:
    Thesis Table 7.5, Bootstrap Contrasts of Indirect Effects.
    Reports the difference of two indirect effects with 95% CI.

HYPOTHESIS TESTED: H3

THESIS REFERENCE:
    Chapter 7, Investigating the Mediating Role of Political Efficacy

INPUT:
    data_cleaned.csv

METHOD:
    Nonparametric bootstrap (5,000 resamples) of the difference between
    two a*b indirect effects, percentile 95% confidence intervals.

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

def boot_indirect(d, m, y, covar, B=5000, seed=1):
    rng = np.random.default_rng(seed)
    n = len(d)
    base = d[["tech_total"] + covar].values
    Xa = np.column_stack([np.ones(n), base])
    M = d[m].values; Y = d[y].values
    out = np.empty(B)
    for i in range(B):
        idx = rng.integers(0, n, n)
        a = np.linalg.lstsq(Xa[idx], M[idx], rcond=None)[0][1]
        Xb = np.column_stack([np.ones(n), d[m].values[idx], base[idx]])
        b = np.linalg.lstsq(Xb, Y[idx], rcond=None)[0][1]
        out[i] = a * b
    return out

pairs = [("Internal-Online vs External-Online", ("internal_eff","online_part"), ("external_eff","online_part")),
         ("External-Traditional vs Internal-Traditional", ("external_eff","trad_part"), ("internal_eff","trad_part")),
         ("Internal: Online vs Traditional", ("internal_eff","online_part"), ("internal_eff","trad_part")),
         ("External: Traditional vs Online", ("external_eff","trad_part"), ("external_eff","online_part"))]
for label, (m1,y1), (m2,y2) in pairs:
    d1 = boot_indirect(df, m1, y1, COVAR, seed=1)
    d2 = boot_indirect(df, m2, y2, COVAR, seed=1)
    diff = d1 - d2
    lo, hi = np.percentile(diff, [2.5, 97.5])
    sig = "Yes" if (lo > 0 or hi < 0) else "No"
    print(f"{label}: diff={diff.mean():.4f}, 95% CI [{lo:.4f}, {hi:.4f}], sig={sig}")

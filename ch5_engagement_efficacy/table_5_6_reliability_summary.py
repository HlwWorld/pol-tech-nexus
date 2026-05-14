"""
================================================================
SCRIPT: table_5_7_reliability_summary.py
================================================================
PURPOSE:
    Cronbach (1951) alpha and McDonald (1999) omega for the nine
    multi-item Likert scales used anywhere in the thesis.

OUTPUT:
    Thesis Table 5.7, Cronbach's Alpha and McDonald's Omega for the
    Nine Likert Scales
    Reports: k, alpha, omega per scale.

HYPOTHESIS TESTED: N/A, measurement diagnostic.

THESIS REFERENCE:
    Chapter 5, Section 5.7, Reliability Analysis.

INPUT:
    data_cleaned.csv

METHOD:
    Cronbach alpha: variance-ratio formula on listwise-complete data.
    McDonald omega: one-factor congeneric approximation derived from
    the first principal component of the inter-item correlation matrix.

DEPENDENCIES:
    pandas, numpy

================================================================
The code is made available only for academic purposes and
verification. Redistribution, reuse, or modification of this
code, in its entirety or in part, will require the author's
written permission.
================================================================
"""
import pandas as pd
import numpy as np

df = pd.read_csv("data_cleaned.csv")
df = df.replace(-99, np.nan)

def cronbach_alpha(d):
    d = d.dropna()
    k = d.shape[1]
    if k < 2:
        return float('nan')
    item_var = d.var(axis=0, ddof=1)
    total_var = d.sum(axis=1).var(ddof=1)
    return (k / (k - 1)) * (1 - item_var.sum() / total_var)

def mcdonald_omega(d):
    d = d.dropna()
    R = d.corr().values
    vals, vecs = np.linalg.eigh(R)
    idx = np.argsort(vals)[::-1]
    L = np.abs(np.sqrt(max(vals[idx[0]], 0)) * vecs[:, idx[0]])
    return (L.sum() ** 2) / (L.sum() ** 2 + (1 - L ** 2).sum())

scales = {
    "B1.5 Social Media Activity":               [f"B1.5_{i}" for i in range(1, 9)],
    "B2.5 Messaging Purpose":                   [f"B2.5_{i}" for i in range(1, 7)],
    "B3.6 University Online Services":          [f"B3.6_{i}" for i in range(1, 8)],
    "B4.4 Online News Content":                 [f"B4.4_{i}" for i in range(1, 9)],
    "C1.1 Traditional Political Participation": [f"C1.1_{i}" for i in range(1, 13)],
    "C2.1 Online Political Participation":      [f"C2.1_{i}" for i in range(1, 15)],
    "C3.1 Political Information Consumption":   [f"C3.1_{i}" for i in range(1, 13)],
    "D1.1 Internal Political Efficacy":         [f"D1.1_{i}" for i in range(1, 9)],
    "D2.1 External Political Efficacy":         [f"D2.1_{i}" for i in range(1, 9)],
}

rows = []
for name, items in scales.items():
    d = df[items]
    rows.append({
        "Scale": name,
        "k": len(items),
        "Cronbach alpha": round(cronbach_alpha(d), 3),
        "McDonald omega": round(mcdonald_omega(d), 3),
    })

print(pd.DataFrame(rows).to_string(index=False))

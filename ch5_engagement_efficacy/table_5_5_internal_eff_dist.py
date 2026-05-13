"""
================================================================
SCRIPT: table_5_5_internal_eff_dist.py
================================================================
PURPOSE:
    Item-level statistics for the Internal Political Efficacy scale
    (D1.1, 8 items), including item-rest correlations and the
    alpha-if-deleted diagnostic.

OUTPUT:
    Thesis Table 5.5, Internal Efficacy Item Statistics
    Reports: M, SD, % Agree (4-5), r (item-rest), alpha-if-deleted.

HYPOTHESIS TESTED: N/A, measurement diagnostic.

THESIS REFERENCE:
    Chapter 5, Section 5.5, Internal Political Efficacy.

INPUT:
    data_cleaned.csv

METHOD:
    Cronbach (1951) alpha; corrected item-total correlation
    (Pearson r between each item and the sum of the remaining items).

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

items = [f"D1.1_{i}" for i in range(1, 9)]
labels = [
    "I consider myself well-qualified to participate in politics",
    "I am better informed about politics than most people",
    "I have a good understanding of important political issues",
    "I could do as good a job in public office as most others",
    "I am confident I can understand complex political issues",
    "I have the skills to participate effectively in politics",
    "I am capable of making informed political decisions",
    "I understand how the Bangladeshi political system works",
]

def cronbach_alpha(d):
    d = d.dropna()
    k = d.shape[1]
    if k < 2:
        return float('nan')
    item_var = d.var(axis=0, ddof=1)
    total_var = d.sum(axis=1).var(ddof=1)
    return (k / (k - 1)) * (1 - item_var.sum() / total_var)

d = df[items].dropna()
overall_alpha = cronbach_alpha(d)

rows = []
for it, lab in zip(items, labels):
    s = df[it].dropna()
    rest = d.drop(columns=[it]).sum(axis=1)
    r_it = float(d[it].corr(rest))
    a_del = cronbach_alpha(d.drop(columns=[it]))
    rows.append({
        "Item": lab,
        "M": round(s.mean(), 2),
        "SD": round(s.std(ddof=1), 2),
        "% Agree": round((s >= 4).sum() / len(s) * 100, 1),
        "r (item-rest)": round(r_it, 3),
        "alpha if deleted": round(a_del, 3),
    })

comp = df[items].mean(axis=1, skipna=True)
rows.append({
    "Item": "Composite (mean of 8 items)",
    "M": round(comp.mean(), 2),
    "SD": round(comp.std(ddof=1), 2),
    "% Agree": "-",
    "r (item-rest)": "-",
    "alpha if deleted": f"alpha = {overall_alpha:.2f}",
})

print(pd.DataFrame(rows).to_string(index=False))
print(f"\nFull-scale Cronbach alpha = {overall_alpha:.3f}")

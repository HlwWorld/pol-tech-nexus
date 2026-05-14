"""
================================================================
SCRIPT: table_5_6_external_eff_dist.py
================================================================
PURPOSE:
    Item-level statistics for the External Political Efficacy scale
    (D2.1, 8 items) after reverse coding of items D2.1_1 to D2.1_4
    (which was applied during the data-cleaning pipeline). Reports
    item-rest correlations and alpha-if-deleted.

OUTPUT:
    Thesis Table 5.6, External Efficacy Item Statistics (Reverse-Coded)
    Reports: M, SD, % Agree (4-5), r (item-rest), alpha-if-deleted.

HYPOTHESIS TESTED: N/A, measurement diagnostic.

THESIS REFERENCE:
    Chapter 5, Section 5.6, External Political Efficacy.

INPUT:
    data_cleaned.csv (items 1-4 already reverse coded)

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

items = [f"D2.1_{i}" for i in range(1, 9)]
labels = [
    "Public officials care about people like me (R)",
    "People like me have a say about what government does (R)",
    "Government officials care about people like me (R)",
    "Elected representatives stay in touch with the people (R)",
    "Government is responsive to ordinary citizens",
    "Voting is an effective way to influence government",
    "Political leaders pay attention to young people",
    "Citizen participation can make a difference",
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
print(f"\nFull-scale Cronbach alpha (after reverse coding) = {overall_alpha:.3f}")

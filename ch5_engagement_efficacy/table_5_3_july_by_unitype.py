"""
================================================================
SCRIPT: table_5_3_july_by_unitype.py
================================================================
PURPOSE:
    Means and standard deviations for the three July 2024 movement-
    related online participation items (C2.1_6, C2.1_10, C2.1_13)
    plus their three-item subscale, broken down by university type
    (Public, Private, NU-affiliated).

OUTPUT:
    Thesis Table 5.3, July 2024 Movement Items by University Type
    Reports: M (SD) for each item by university type and overall.

HYPOTHESIS TESTED: N/A, descriptive only. Formal group-difference
    test of H4 lives in Chapter 8.

THESIS REFERENCE:
    Chapter 5, Section 5.3.2, July 2024 Movement-Related Activities.

INPUT:
    data_cleaned.csv

METHOD:
    Replace valid-skip code -99 with NaN. Group means and SDs by
    A2_Type (1 = Public, 2 = Private, 3 = NU).

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

july_items = ["C2.1_6", "C2.1_10", "C2.1_13"]
labels = {
    "C2.1_6":  "Used a political hashtag (e.g., #JulyRevolution)",
    "C2.1_10": "Shared information about protests online",
    "C2.1_13": "Watched live political events online",
}

type_names = {1: "Public", 2: "Private", 3: "NU"}

def fmt(s):
    return f"{s.mean():.2f} ({s.std(ddof=1):.2f})"

rows = []
for it in july_items:
    row = {"Item": labels[it]}
    for t, name in type_names.items():
        s = df.loc[df["A2_Type"] == t, it].dropna()
        row[f"{name} M (SD)"] = fmt(s)
    s_all = df[it].dropna()
    row["Overall M (SD)"] = fmt(s_all)
    rows.append(row)

# Three-item subscale
df["c21_july"] = df[july_items].mean(axis=1, skipna=True)
row = {"Item": "Three-item July 2024 subscale"}
for t, name in type_names.items():
    s = df.loc[df["A2_Type"] == t, "c21_july"].dropna()
    row[f"{name} M (SD)"] = fmt(s)
row["Overall M (SD)"] = fmt(df["c21_july"].dropna())
rows.append(row)

print(pd.DataFrame(rows).to_string(index=False))

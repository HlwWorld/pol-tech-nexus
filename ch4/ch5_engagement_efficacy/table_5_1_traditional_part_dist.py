"""
================================================================
SCRIPT: table_5_1_traditional_part_dist.py
================================================================
PURPOSE:
    Produce item-level descriptive statistics for the Traditional
    Political Participation scale (C1.1, 12 items) on the 1 to 5
    Likert metric, plus the composite mean.

OUTPUT:
    Thesis Table 5.1, Traditional Political Participation Frequencies
    Reports: n, M, SD, % High (4-5), % Low (1-2) for each item.

HYPOTHESIS TESTED: N/A, descriptive only.

THESIS REFERENCE:
    Chapter 5, Section 5.2, Traditional Political Participation.

INPUT:
    data_cleaned.csv

METHOD:
    Replace valid-skip code -99 with NaN. Compute item-level frequencies
    and Likert-mean descriptives.

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

items = [f"C1.1_{i}" for i in range(1, 13)]
labels = [
    "Voted in a national election (or plan to)",
    "Voted in a local/municipal election (or plan to)",
    "Attended a political rally or public meeting",
    "Participated in a protest or demonstration",
    "Contacted a government official",
    "Contacted a local leader",
    "Joined a political party",
    "Joined a student political organization",
    "Volunteered for a political campaign",
    "Donated to a political party or candidate",
    "Attended a town hall or public consultation",
    "Worked with others on a community problem",
]

rows = []
for item, lab in zip(items, labels):
    s = df[item].dropna()
    rows.append({
        "Item": lab,
        "n": int(s.count()),
        "M": round(s.mean(), 2),
        "SD": round(s.std(ddof=1), 2),
        "% High (4-5)": round((s >= 4).sum() / len(s) * 100, 1),
        "% Low (1-2)": round((s <= 2).sum() / len(s) * 100, 1),
    })

# Composite
comp = df[items].mean(axis=1, skipna=True)
rows.append({
    "Item": "Composite (mean of 12 items)",
    "n": int(comp.count()),
    "M": round(comp.mean(), 2),
    "SD": round(comp.std(ddof=1), 2),
    "% High (4-5)": "-",
    "% Low (1-2)": "-",
})

out = pd.DataFrame(rows)
print(out.to_string(index=False))

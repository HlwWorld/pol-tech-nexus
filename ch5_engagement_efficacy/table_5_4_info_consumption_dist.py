"""
================================================================
SCRIPT: table_5_4_info_consumption_dist.py
================================================================
PURPOSE:
    Item-level descriptive statistics for the Political Information
    Consumption scale (C3.1, 12 items).

OUTPUT:
    Thesis Table 5.4, Political Information Consumption Frequencies
    Reports: n, M, SD, % High (4-5) for each item.

HYPOTHESIS TESTED: N/A, descriptive only.

THESIS REFERENCE:
    Chapter 5, Section 5.4, Political Information Consumption.

INPUT:
    data_cleaned.csv

METHOD:
    Replace valid-skip code -99 with NaN. Compute item-level
    frequencies and Likert-mean descriptives.

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

items = [f"C3.1_{i}" for i in range(1, 13)]
labels = [
    "Follow news about national politics",
    "Follow news about local/municipal politics",
    "Follow news about international politics",
    "Read political news from multiple sources",
    "Discuss political issues with friends",
    "Discuss political issues with family",
    "Discuss politics with classmates/colleagues",
    "Seek information about candidates/parties",
    "Seek information about government policies",
    "Read political analysis or opinion pieces",
    "Watch political debates online/TV",
    "Try to understand different perspectives",
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
    })

comp = df[items].mean(axis=1, skipna=True)
rows.append({
    "Item": "Composite (mean of 12 items)",
    "n": int(comp.count()),
    "M": round(comp.mean(), 2),
    "SD": round(comp.std(ddof=1), 2),
    "% High (4-5)": "-",
})

print(pd.DataFrame(rows).to_string(index=False))

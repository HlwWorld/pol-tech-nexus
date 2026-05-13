"""
================================================================
SCRIPT: table_5_2_online_part_dist.py
================================================================
PURPOSE:
    Item-level descriptive statistics for the Online Political
    Participation scale (C2.1, 14 items). The three items flagged
    with an asterisk (C2.1_6, C2.1_10, C2.1_13) target the
    July 2024 quota-reform movement; they are also analyzed in
    table_5_3_by_unitype.py.

OUTPUT:
    Thesis Table 5.2, Online Political Participation Frequencies
    Reports: n, M, SD, % High (4-5), % Low (1-2) for each item.

HYPOTHESIS TESTED: N/A, descriptive only.

THESIS REFERENCE:
    Chapter 5, Section 5.3, Online Political Participation.

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

items = [f"C2.1_{i}" for i in range(1, 15)]
labels = [
    "Signed an online petition",
    "Shared political news on social media",
    "Posted original political opinions",
    "Commented on political posts",
    "Participated in online political discussions",
    "Used a political hashtag (e.g., #JulyRevolution)*",
    "Joined an online political group",
    "Followed political leaders/activists",
    "Liked or reacted to political content",
    "Shared information about protests*",
    "Contacted an official via email/social media",
    "Participated in online political surveys",
    "Watched live political events online*",
    "Created/shared political memes or visuals",
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

comp = df[items].mean(axis=1, skipna=True)
rows.append({
    "Item": "Composite (mean of 14 items)",
    "n": int(comp.count()),
    "M": round(comp.mean(), 2),
    "SD": round(comp.std(ddof=1), 2),
    "% High (4-5)": "-",
    "% Low (1-2)": "-",
})

print(pd.DataFrame(rows).to_string(index=False))

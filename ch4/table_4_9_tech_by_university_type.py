"""
Table 4.9 – Technology dimension and tech_total scores by university type, mean (SD) (n = 472)
"""
import pandas as pd, numpy as np

df = pd.read_csv('../data_cleaned.csv')
df.replace(-99, np.nan, inplace=True)

TYPES  = {1: 'Public', 2: 'Private', 3: 'NU'}
SCORES = {
    'social_media_score': 'Social media score',
    'messaging_score':    'Messaging score',
    'egovt_score':        'E-government score',
    'online_news_score':  'Online news score',
    'tech_total':         'tech_total',
}

rows = []
for col, label in SCORES.items():
    row = [label]
    for t, name in TYPES.items():
        sub = df[df.A2_Type == t][col]
        row.append(f"{sub.mean():.3f} ({sub.std():.3f})")
    rows.append(row)

result = pd.DataFrame(rows,
    columns=['Score',
             f'Public (n=188)', f'Private (n=190)', f'NU (n=94)'])

print("Table 4.9 – Technology Dimension and tech_total Scores by University Type, Mean (SD)\n")
print(result.to_string(index=False))
print("\nNote. All scores are MinMax-normalized to the 0–1 interval. "
      "No significance tests are reported in this chapter; "
      "inferential comparisons appear in Chapter 8.")

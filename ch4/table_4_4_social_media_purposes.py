"""
Table 4.4 – Social media purposes (B1.4) and Likert behaviors (B1.5) (n = 472)
"""
import pandas as pd
import numpy as np

df = pd.read_csv('data_cleaned.csv')
df.replace(-99, np.nan, inplace=True)

PURPOSE_COLS = {
    'B1.4_1_FriendsFamily': 'Friends and family',
    'B1.4_2_Entertainment': 'Entertainment',
    'B1.4_3_NewsCurrent':   'News and current events',
    'B1.4_4_Educational':   'Educational content',
    'B1.4_5_Professional':  'Professional networking',
    'B1.4_6_PoliticalInfo': 'Political information and discussion',
    'B1.4_7_Shopping':      'Shopping / e-commerce',
}

LIKERT_LABELS = {
    'B1.5_1': 'Check news feeds for general information',
    'B1.5_2': 'Watch news videos',
    'B1.5_3': 'Read articles shared by others',
    'B1.5_4': 'Follow news pages or accounts',
    'B1.5_5': 'Share or repost information',
    'B1.5_6': 'Engage in discussions',
    'B1.5_7': 'Comment on posts',
    'B1.5_8': 'Follow political leaders or activists',
}

rows = []
rows.append(['B1.4 – Purposes of use (% selected, multiple-response)', '', ''])
for col, label in PURPOSE_COLS.items():
    valid = df[col].notna().sum()
    n = df[col].sum()
    pct = n / valid * 100
    rows.append(['', label, f"{pct:.1f}%"])

rows.append(['', '', ''])
rows.append(['B1.5 – Activity behaviors (1=never to 5=very often)', 'Mean', 'SD'])
for col, label in LIKERT_LABELS.items():
    m  = df[col].mean()
    sd = df[col].std()
    rows.append(['', label, f"{m:.2f}   {sd:.2f}"])

result = pd.DataFrame(rows, columns=['Item', 'Mean / %', 'SD'])

print("Table 4.4 – Social Media Purposes and Likert Behaviors\n")
print(result.to_string(index=False))
print(f"\nNote. B1.4 % based on valid (non-missing) responses per item. "
      f"B1.5 items on 1–5 Likert scale; -99 treated as missing.")

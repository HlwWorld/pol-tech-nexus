"""
Table 4.4 – Social media purposes (B1.4) and Likert behaviors (B1.5) (n = 472)
"""
import pandas as pd, numpy as np

df = pd.read_csv('../data_cleaned.csv')
df.replace(-99, np.nan, inplace=True)
N = len(df)

PURPOSE_COLS = {
    'B1.4_1_FriendsFamily':  'Staying in touch with friends/family',
    'B1.4_2_Entertainment':  'Entertainment',
    'B1.4_3_NewsCurrent':    'Following news and current events',
    'B1.4_4_Educational':    'Educational content',
    'B1.4_5_Professional':   'Professional networking',
    'B1.4_6_PoliticalInfo':  'Political information and discussion',
    'B1.4_7_Shopping':       'Shopping/e-commerce',
    'B1.4_8_Other':          'Other',
}
LIKERT_LABELS = {
    'B1.5_1': 'Share political news or current events',
    'B1.5_2': 'Comment on political posts',
    'B1.5_3': 'Follow political leaders/organisations',
    'B1.5_4': 'Share news about community issues',
    'B1.5_5': 'Join/follow civic or political groups',
    'B1.5_6': 'Sign or share online petitions',
    'B1.5_7': 'Discuss political topics with contacts',
    'B1.5_8': 'Encourage others to vote or participate',
}

rows = []
rows.append(['B1.4 – Purposes of use (% selecting)', '', ''])
for col, label in PURPOSE_COLS.items():
    n = df[col].sum()
    rows.append(['', label, f"{n/N*100:.1f}%"])

rows.append(['', '', ''])
rows.append(['B1.5 – Activity behaviors (1=never to 5=very often)', 'Mean', 'SD'])
for col, label in LIKERT_LABELS.items():
    m  = df[col].mean()
    sd = df[col].std()
    rows.append(['', label, f"{m:.2f}   {sd:.2f}"])

result = pd.DataFrame(rows, columns=['Item', 'Mean / %', 'SD'])

print("Table 4.4 – Social Media Purposes and Likert Behaviors\n")
print(result.to_string(index=False))
print(f"\nNote. B1.4 % of all N = {N} respondents. "
      f"B1.5 items on 1–5 Likert scale; -99 treated as missing.")

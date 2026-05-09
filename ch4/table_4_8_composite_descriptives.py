"""
Table 4.8 – Descriptive statistics for technology dimension scores and tech_total (n = 472)
"""
import pandas as pd, numpy as np

df = pd.read_csv('../data_cleaned.csv')
df.replace(-99, np.nan, inplace=True)
N = len(df)

SCORES = {
    'social_media_score': 'Social media score',
    'messaging_score':    'Messaging score',
    'egovt_score':        'E-government score',
    'online_news_score':  'Online news score',
    'tech_total':         'tech_total (composite)',
}

rows = []
for col, label in SCORES.items():
    d = df[col].dropna()
    rows.append([
        label, len(d),
        f"{d.mean():.3f}", f"{d.std():.3f}",
        f"{d.min():.3f}", f"{d.max():.3f}",
        f"{d.skew():.2f}", f"{d.kurt():.2f}",
    ])

result = pd.DataFrame(rows,
    columns=['Score', 'n', 'M', 'SD', 'Min', 'Max', 'Skew', 'Kurtosis'])

print("Table 4.8 – Descriptive Statistics for Technology Dimension Scores and tech_total\n")
print(result.to_string(index=False))
print("\nNote. All scores are MinMax-normalized to the 0–1 interval. "
      "tech_total is the arithmetic mean of the four dimension scores. "
      "Skewness and excess kurtosis are reported.")

"""
Table 4.7 – Online news frequency, time, sources, content types, and access modes (n = 472)
"""
import pandas as pd, numpy as np

df = pd.read_csv('../data_cleaned.csv')
df.replace(-99, np.nan, inplace=True)
N = len(df)

FREQ_LABELS = {
    1: 'Multiple times a day', 2: 'Once a day',
    3: 'A few times a week', 4: 'Once a week',
    5: 'Less than once a week', 6: 'Never',
}
TIME_LABELS = {
    1: 'Less than 15 min', 2: '15 – 30 min',
    3: '30 min – 1 hour', 4: '1 – 2 hours',
    5: 'More than 2 hours',
}
SOURCE_COLS = {
    'B4.3_1_BDNewspapers':   'Bangladeshi online newspapers',
    'B4.3_2_IntNews':        'International news websites',
    'B4.3_3_BDYouTubeNews':  'Bangladeshi YouTube news channels',
    'B4.3_4_IntYouTubeNews': 'International YouTube news channels',
    'B4.3_5_Aggregators':    'News aggregators / apps',
    'B4.3_6_Podcasts':       'News podcasts',
    'B4.3_7_OnlinePortals':  'Online news portals',
    'B4.3_8_Other':          'Other',
}
CONTENT_COLS = {
    'B4.4_1': 'National/domestic news',
    'B4.4_2': 'Local community news',
    'B4.4_3': 'International news',
    'B4.4_4': 'Political news',
    'B4.4_5': 'Business/economic news',
    'B4.4_6': 'Sports news',
    'B4.4_7': 'Technology news',
    'B4.4_8': 'Entertainment news',
}
ACCESS_COLS = {
    'B4.5_1_DirectWebsite':  'Direct website/app visit',
    'B4.5_2_SocialFeeds':    'Social media feeds',
    'B4.5_3_AggregatorApp':  'News aggregator app',
    'B4.5_4_SearchEngine':   'Search engine',
    'B4.5_5_MsgLinks':       'Messaging app links',
    'B4.5_6_YouTubeSub':     'YouTube subscriptions',
    'B4.5_7_Other':          'Other',
}

rows = []
valid_f = df['B4.1_FreqOnlineNews'].notna().sum()
rows.append(['Online news frequency (B4.1)', f'% (valid n={valid_f})', ''])
for code, label in FREQ_LABELS.items():
    n = (df['B4.1_FreqOnlineNews'] == code).sum()
    rows.append([label, f"{n} ({n/valid_f*100:.1f}%)", ''])

rows.append(['', '', ''])
valid_t = df['B4.2_TimeNews'].notna().sum()
rows.append(['Daily time on news (B4.2)', f'% (valid n={valid_t})', ''])
for code, label in TIME_LABELS.items():
    n = (df['B4.2_TimeNews'] == code).sum()
    rows.append([label, f"{n} ({n/valid_t*100:.1f}%)", ''])

rows.append(['', '', ''])
rows.append(['News sources (B4.3 – multiple select)', f'% (n={N})', ''])
for col, label in SOURCE_COLS.items():
    valid = df[col].notna().sum()
    n = df[col].sum()
    rows.append([label, f"{n:.0f} ({n/valid*100:.1f}%)", ''])

rows.append(['', '', ''])
rows.append(['Content-type preference (B4.4, 1–5 Likert)', 'Mean', 'SD'])
for col, label in CONTENT_COLS.items():
    m  = df[col].mean()
    sd = df[col].std()
    rows.append([label, f"{m:.2f}", f"{sd:.2f}"])

rows.append(['', '', ''])
rows.append(['Access mode (B4.5 – multiple select)', f'% (n={N})', ''])
for col, label in ACCESS_COLS.items():
    valid = df[col].notna().sum()
    n = df[col].sum()
    rows.append([label, f"{n:.0f} ({n/valid*100:.1f}%)", ''])

result = pd.DataFrame(rows, columns=['Item', '% / M (SD)', ''])
print("Table 4.7 – Online News Frequency, Time, Sources, Content, and Access Modes\n")
print(result.to_string(index=False))
print(f"\nNote. N = {N}. Multiple-select columns report percentage of valid respondents.")

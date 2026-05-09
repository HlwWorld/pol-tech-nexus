"""
Table 4.5 – Messaging application adoption, time, frequency, and Likert purposes (n = 472)
"""
import pandas as pd, numpy as np

df = pd.read_csv('../data_cleaned.csv')
df.replace(-99, np.nan, inplace=True)
N = len(df)

pub = df[df.A2_Type == 1]
prv = df[df.A2_Type == 2]
nu  = df[df.A2_Type == 3]

APP_COLS = {
    'B2.1_1_FBMessenger': 'Facebook Messenger',
    'B2.1_2_WhatsApp':    'WhatsApp',
    'B2.1_3_Telegram':    'Telegram',
    'B2.1_4_Viber':       'Viber',
    'B2.1_5_IMO':         'IMO',
    'B2.1_6_Signal':      'Signal',
    'B2.1_7_WeChat':      'WeChat',
    'B2.1_8_None':        'None',
}
TIME_LABELS = {
    1: 'Less than 30 min', 2: '30 min – 1 hour',
    3: '1 – 2 hours', 4: '2 – 3 hours',
    5: '3 – 4 hours', 6: 'More than 4 hours',
}
FREQ_LABELS = {
    1: 'Several times per day', 2: 'Once a day',
    3: 'A few times per week', 4: 'Once a week',
    5: 'Less than once a week',
}
GROUP_LABELS = {
    1: 'No group chats', 2: '1 – 3 groups',
    3: '4 – 6 groups', 4: '7 – 10 groups',
    5: 'More than 10 groups',
}
LIKERT_LABELS = {
    'B2.5_1': 'Personal communication',
    'B2.5_2': 'Academic discussion',
    'B2.5_3': 'News sharing',
    'B2.5_4': 'Political discussion',
    'B2.5_5': 'Civic/community coordination',
    'B2.5_6': 'Professional networking',
}

rows = []
rows.append(['App adoption (B2.1)', '% Overall', 'M (SD)'])
for col, label in APP_COLS.items():
    pct  = df[col].mean() * 100
    ppub = pub[col].mean() * 100
    pprv = prv[col].mean() * 100
    pnu  = nu[col].mean()  * 100
    rows.append([label, f"{pct:.1f}%", f"Pub {ppub:.0f}% / Prv {pprv:.0f}% / NU {pnu:.0f}%"])

rows.append(['', '', ''])
rows.append(['Daily time on messaging (B2.2)', '%', ''])
valid_t = df['B2.2_TimeMsg'].notna().sum()
for code, label in TIME_LABELS.items():
    n = (df['B2.2_TimeMsg'] == code).sum()
    rows.append([label, f"{n} ({n/valid_t*100:.1f}%)", ''])

rows.append(['', '', ''])
rows.append(['Frequency (B2.3)', '%', ''])
valid_f = df['B2.3_FreqMsg'].notna().sum()
for code, label in FREQ_LABELS.items():
    n = (df['B2.3_FreqMsg'] == code).sum()
    rows.append([label, f"{n} ({n/valid_f*100:.1f}%)", ''])

rows.append(['', '', ''])
rows.append(['Group-chat membership (B2.4)', '%', ''])
valid_g = df['B2.4_GroupChats'].notna().sum()
for code, label in GROUP_LABELS.items():
    n = (df['B2.4_GroupChats'] == code).sum()
    rows.append([label, f"{n} ({n/valid_g*100:.1f}%)", ''])

rows.append(['', '', ''])
rows.append(['B2.5 Likert behaviors (1–5)', 'Mean', 'SD'])
for col, label in LIKERT_LABELS.items():
    m  = df[col].mean()
    sd = df[col].std()
    rows.append([label, f"{m:.2f}", f"{sd:.2f}"])

result = pd.DataFrame(rows, columns=['Item', '%', 'M (SD)'])
print("Table 4.5 – Messaging Application Adoption, Time, Frequency, and Likert Purposes\n")
print(result.to_string(index=False))
print(f"\nNote. N = {N}. Valid n varies by item due to valid skips.")

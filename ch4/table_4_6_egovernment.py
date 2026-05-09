"""
Table 4.6 – E-government and university-online service utilization (n = 472)
"""
import pandas as pd, numpy as np

df = pd.read_csv('../data_cleaned.csv')
df.replace(-99, np.nan, inplace=True)
N = len(df)

EGOV_USE_LABELS = {
    1: 'Frequent use', 2: 'Occasional use',
    3: 'Once or twice', 4: 'Never used',
}
EGOV_SVC_COLS = {
    'B3.2_1_NID':      'National ID card (NID) services',
    'B3.2_2_Passport': 'Passport application/renewal',
    'B3.2_3_BirthCert':'Birth certificate',
    'B3.2_4_EduCert':  'Educational certificate verification',
    'B3.2_5_Tax':       'Tax registration/return',
    'B3.2_6_Land':      'Land records',
    'B3.2_7_JobApply':  'Government job application',
    'B3.2_8_Other':     'Other e-gov services',
}
UNI_SVC_LABELS = {
    1: 'University offers online services',
    2: 'No online services',
    3: 'Uncertain',
}
UNI_SVC_COLS = {
    'B3.6_1': 'Online course registration',
    'B3.6_2': 'Result/grade access',
    'B3.6_3': 'Library/e-resource access',
    'B3.6_4': 'Fee payment',
    'B3.6_5': 'Certificate/document request',
    'B3.6_6': 'Admit card/hall ticket',
    'B3.6_7': 'Student portal/dashboard',
}

rows = []
rows.append(['E-government use (B3.1)', '% / M (SD)', 'Valid n'])
valid_b31 = df['B3.1_EGovUse'].notna().sum()
for code, label in EGOV_USE_LABELS.items():
    n = (df['B3.1_EGovUse'] == code).sum()
    rows.append([label, f"{n} ({n/valid_b31*100:.1f}%)", str(valid_b31)])

rows.append(['', '', ''])
rows.append(['E-government services used (B3.2 – multiple select)', '%', f'n={N}'])
for col, label in EGOV_SVC_COLS.items():
    n = df[col].sum()
    rows.append([label, f"{n:.0f} ({n/N*100:.1f}%)", ''])

rows.append(['', '', ''])
rows.append(['University online services (B3.4)', '%', f'n={N}'])
for code, label in UNI_SVC_LABELS.items():
    n = (df['B3.4_UniOnlineYes'] == code).sum()
    rows.append([label, f"{n} ({n/N*100:.1f}%)", ''])

rows.append(['', '', ''])
valid_uni = (df['B3.4_UniOnlineYes'] == 1).sum()
rows.append([f'University service use – Likert (B3.6, 1–5; valid n={valid_uni})', 'M (SD)', ''])
uni_yes = df[df['B3.4_UniOnlineYes'] == 1]
for col, label in UNI_SVC_COLS.items():
    m  = uni_yes[col].mean()
    sd = uni_yes[col].std()
    vn = uni_yes[col].notna().sum()
    rows.append([label, f"{m:.2f} ({sd:.2f})", str(vn)])

result = pd.DataFrame(rows, columns=['Item', '% / M (SD)', 'Valid n'])
print("Table 4.6 – E-Government and University-Online Service Utilization\n")
print(result.to_string(index=False))
print(f"\nNote. Valid n for B3.6 reflects respondents whose university offers services (n={valid_uni}).")

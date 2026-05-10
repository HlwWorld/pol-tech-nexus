"""
Table 4.6 - E-government and university-online service utilization (n = 472)

Reproduces every figure shown in Chapter 4, Table 4.6:
  - B3.1  Frequency of e-government service use            (valid-n base)
  - B3.2  Service categories used (multiple-response)      (n = 472 base)
  - B3.3  Experience with e-government services            (n = 472 base)
  - B3.4  University offers online services                (n = 472 base)
  - B3.5  Frequency of using university online platforms   (valid-n base)
  - B3.6  University-online services - Likert 1 to 5       (B3.4 == 1 subset,
                                                            valid-n per item)

Notes
-----
* B3.6 means and SDs are computed only on respondents whose university
  reports having online services (B3.4 == 1, n = 368). Within that subset,
  structurally unavailable items (e.g. course registration at NU and most
  honours-level public programmes; fee payment at JU honours) are valid
  skips coded -99 in the cleaned file and treated as NaN, so item-level
  valid n varies across the seven services.
* Column names follow the cleaned-data dictionary; B3.6 labels follow the
  questionnaire mapping (B3.6_1 = student portal, _2 = LMS, _3 = course
  registration, _4 = result/grade checking, _5 = digital library,
  _6 = fee payment, _7 = university email).
"""
import pandas as pd
import numpy as np

df = pd.read_csv('data_cleaned.csv')
df.replace(-99, np.nan, inplace=True)
N = len(df)

EGOV_USE_LABELS = {
    1: 'Yes, frequently',
    2: 'Yes, occasionally',
    3: 'Once or twice',
    4: 'No, never',
}

EGOV_SVC_COLS = {
    'B3.2_1_NID':       'National ID services',
    'B3.2_4_EduCert':   'Educational certificate verification',
    'B3.2_2_Passport':  'Passport application or renewal',
    'B3.2_3_BirthCert': 'Birth or death certificate',
    'B3.2_7_JobApply':  'Government job applications',
    'B3.2_5_Tax':       'Tax-related services',
    'B3.2_6_Land':      'Land or property records',
    'B3.2_8_Other':     'Other e-government services',
}

EGOV_EXP_LABELS = {
    1: 'Very satisfactory',
    2: 'Satisfactory',
    3: 'Neutral',
    4: 'Unsatisfactory',
    5: 'Very unsatisfactory',
    6: 'Have not used',
}

UNI_AVAIL_LABELS = {
    1: 'Yes',
    2: 'No',
    3: 'Do not know',
}

UNI_FREQ_LABELS = {
    1: 'Daily',
    2: 'Several times per week',
    3: 'Once a week',
    4: 'A few times per month',
    5: 'Rarely',
    6: 'Never',
    7: 'Not applicable',
}

# B3.6 (CORRECT mapping per questionnaire), ordered by mean (descending)
UNI_SVC_COLS = {
    'B3.6_4': 'Online result or grade checking',
    'B3.6_6': 'Online fee payment',
    'B3.6_3': 'Online course registration',
    'B3.6_1': 'Student portal',
    'B3.6_7': 'University email',
    'B3.6_2': 'Learning Management System (LMS)',
    'B3.6_5': 'Digital library',
}

rows = []
rows.append(['Item', '% / M (SD)', 'Valid n'])

# B3.1
valid_b31 = df['B3.1_EGovUse'].notna().sum()
rows.append(['B3.1 Frequency of e-government service use', '', ''])
for code, label in EGOV_USE_LABELS.items():
    n = (df['B3.1_EGovUse'] == code).sum()
    rows.append([label, f"{n/valid_b31*100:.1f}%", str(valid_b31)])

# B3.2
rows.append(['B3.2 Service categories used (multiple-response)', '', ''])
for col, label in EGOV_SVC_COLS.items():
    n = df[col].sum()
    rows.append([label, f"{n/N*100:.1f}%", str(N)])

# B3.3
rows.append(['B3.3 Experience with e-government services', '', ''])
for code, label in EGOV_EXP_LABELS.items():
    n = (df['B3.3_EGovExperience'] == code).sum()
    rows.append([label, f"{n/N*100:.1f}%", str(N)])

# B3.4
rows.append(['B3.4 University offers online services', '', ''])
for code, label in UNI_AVAIL_LABELS.items():
    n = (df['B3.4_UniOnlineYes'] == code).sum()
    rows.append([label, f"{n/N*100:.1f}%", str(N)])

# B3.5 (percentages reported on the valid-n base, consistent with B3.1)
valid_b35 = df['B3.5_UniFreq'].notna().sum()
rows.append(['B3.5 Frequency of using university online platforms', '', ''])
for code, label in UNI_FREQ_LABELS.items():
    n = (df['B3.5_UniFreq'] == code).sum()
    rows.append([label, f"{n/valid_b35*100:.1f}%", str(valid_b35)])

# B3.6 (Likert; subset = university provides online services)
uni_yes = df[df['B3.4_UniOnlineYes'] == 1]
n_b34_yes = len(uni_yes)
rows.append(['B3.6 University-online services (Likert 1 to 5)', '', ''])
for col, label in UNI_SVC_COLS.items():
    m  = uni_yes[col].mean()
    sd = uni_yes[col].std()
    vn = uni_yes[col].notna().sum()
    rows.append([label, f"{m:.2f} ({sd:.2f})", str(vn)])

result = pd.DataFrame(rows[1:], columns=rows[0])
print("Table 4.6 - E-Government and University-Online Service Utilization\n")
print(result.to_string(index=False))

note = (
    "\nNote. Total N = " + str(N) + ". "
    "Valid n for B3.1 and B3.5 reflects respondents who answered the "
    "respective single-response item; percentages within those blocks "
    "are reported on the valid-n base (consistent with B3.1). "
    "B3.2, B3.3, and B3.4 use the full N = " + str(N) + " base. "
    "Valid n for each B3.6 item reflects respondents whose university "
    "offers that specific service (subset n = " + str(n_b34_yes) + ", "
    "B3.4 == 1)."
)
print(note)

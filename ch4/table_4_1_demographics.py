"""
Table 4.1 – Demographic profile of respondents (n = 472)
Produces: console output matching thesis Table 4.1
"""
import pandas as pd, numpy as np

df = pd.read_csv('../data_cleaned.csv')
N = len(df)  # 472

UNI_LABEL = {
    1: 'University of Dhaka', 2: 'Jahangirnagar University',
    3: "Jagannath University", 4: 'BUET',
    5: 'BRAC University', 6: 'North South University',
    7: 'East West University', 8: 'DIU',
    9: 'UAP', 10: 'Dhaka City College',
    11: 'Tejgaon College', 12: 'Mirpur College',
    13: 'Savar Govt. College',
}
TYPE_LABEL = {1: 'Public', 2: 'Private', 3: 'NU'}
MAJOR_LABEL = {
    1: 'Social Sciences', 2: 'Humanities',
    3: 'Business Studies', 4: 'Natural Sciences',
    5: 'Engineering/Technology',
}
YEAR_LABEL = {
    1: "Honours 1st", 2: "Honours 2nd",
    3: "Honours 3rd", 4: "Honours 4th",
    5: "Master's",
}

def pct(n, tot): return f"{n} ({n/tot*100:.1f}%)"

pub = df[df.A2_Type == 1]
prv = df[df.A2_Type == 2]
nu  = df[df.A2_Type == 3]

rows = []

# --- Gender ---
rows.append(('Gender', '', '', '', '', ''))
for code, label in [(1,'Male'), (2,'Female')]:
    p = (pub.A5_Gender == code).sum()
    r = (prv.A5_Gender == code).sum()
    n = (nu.A5_Gender  == code).sum()
    t = (df.A5_Gender  == code).sum()
    rows.append(('', label,
                 pct(p,len(pub)), pct(r,len(prv)), pct(n,len(nu)),
                 pct(t, N)))

# --- University type ---
rows.append(('University Type', '', '', '', '', ''))
for code, label in TYPE_LABEL.items():
    cnt = (df.A2_Type == code).sum()
    rows.append(('', label, '-', '-', '-', pct(cnt, N)))

# --- Academic year ---
rows.append(('Academic Year', '', '', '', '', ''))
for code, label in YEAR_LABEL.items():
    p = (pub.A3_Year == code).sum()
    r = (prv.A3_Year == code).sum()
    n = (nu.A3_Year  == code).sum()
    t = (df.A3_Year  == code).sum()
    rows.append(('', label,
                 pct(p,len(pub)), pct(r,len(prv)), pct(n,len(nu)),
                 pct(t, N)))

# --- Academic major ---
rows.append(('Academic Major', '', '', '', '', ''))
for code, label in MAJOR_LABEL.items():
    p = (pub.A4_Major == code).sum()
    r = (prv.A4_Major == code).sum()
    n = (nu.A4_Major  == code).sum()
    t = (df.A4_Major  == code).sum()
    rows.append(('', label,
                 pct(p,len(pub)), pct(r,len(prv)), pct(n,len(nu)),
                 pct(t, N)))

# --- Age ---
rows.append(('Age (years)', '', '', '', '', ''))
rows.append(('', f'Mean (SD)',
             f"{pub.A6_Age.mean():.2f} ({pub.A6_Age.std():.2f})",
             f"{prv.A6_Age.mean():.2f} ({prv.A6_Age.std():.2f})",
             f"{nu.A6_Age.mean():.2f}  ({nu.A6_Age.std():.2f})",
             f"{df.A6_Age.mean():.2f}  ({df.A6_Age.std():.2f})"))

result = pd.DataFrame(rows,
    columns=['Variable','Category','Public','Private','NU','Total'])

print(f"Table 4.1 – Demographic Profile (N = {N})\n")
print(result.to_string(index=False))
print(f"\nNote. Public n={len(pub)}, Private n={len(prv)}, NU n={len(nu)}.")

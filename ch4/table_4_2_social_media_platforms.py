"""
Table 4.2 – Social media platform usage by university type (n = 472)
"""
import pandas as pd

df = pd.read_csv('../data_cleaned.csv')
N = len(df)

pub = df[df.A2_Type == 1]; np_ = len(pub)
prv = df[df.A2_Type == 2]; nr  = len(prv)
nu  = df[df.A2_Type == 3]; nu_ = len(nu)

PLATFORMS = [
    ('B1.1_1_Facebook',   'Facebook'),
    ('B1.1_4_WhatsApp',   'WhatsApp'),
    ('B1.1_6_YouTube',    'YouTube'),
    ('B1.1_3_Instagram',  'Instagram'),
    ('B1.1_7_TikTok',     'TikTok'),
    ('B1.1_5_Telegram',   'Telegram'),
    ('B1.1_2_X',          'X (Twitter)'),
    ('B1.1_8_LinkedIn',   'LinkedIn'),
    ('B1.1_9_Snapchat',   'Snapchat'),
    ('B1.1_10_Reddit',    'Reddit'),
]

rows = []
for col, label in PLATFORMS:
    ov = df[col].mean() * 100
    pb = pub[col].mean() * 100
    pv = prv[col].mean() * 100
    pn = nu[col].mean()  * 100
    rows.append([label, f"{ov:.1f}%", f"{pb:.1f}%", f"{pv:.1f}%", f"{pn:.1f}%"])

result = pd.DataFrame(rows,
    columns=['Platform', 'Overall %', 'Public %', 'Private %', 'NU %'])

# Mean platforms per respondent
plat_cols = [c for c in df.columns if c.startswith('B1.1_') and c != 'B1.1_11_None' and c != 'B1.1_12_Other']
df['n_platforms'] = df[plat_cols].sum(axis=1)

print("Table 4.2 – Social Media Platform Usage by University Type\n")
print(result.to_string(index=False))
print(f"\nMean platforms per respondent: {df['n_platforms'].mean():.2f} "
      f"(SD = {df['n_platforms'].std():.2f})")
for t, sub, name in [(1,pub,'Public'),(2,prv,'Private'),(3,nu,'NU')]:
    sub = sub.copy()
    sub['n_p'] = sub[plat_cols].sum(axis=1)
    print(f"  {name}: M={sub['n_p'].mean():.2f}, SD={sub['n_p'].std():.2f}")
print("\nNote. Multiple selection permitted; rows do not sum to 100%.")

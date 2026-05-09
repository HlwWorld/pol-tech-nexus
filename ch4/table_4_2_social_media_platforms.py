"""
Table 4.2 – Social media platform usage by university type (n = 471)
1 non-user (B1.1_11_None == 1) excluded from platform-level analysis.
"""
import pandas as pd

df = pd.read_csv('data_cleaned.csv')

# Exclude the single respondent who reported using no social media
df = df[df['B1.1_11_None'] != 1].copy()

N    = len(df)
pub  = df[df.A2_Type == 1]; n_pub = len(pub)
prv  = df[df.A2_Type == 2]; n_prv = len(prv)
nu   = df[df.A2_Type == 3]; n_nu  = len(nu)

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
    ov = df[col].mean()  * 100
    pb = pub[col].mean() * 100
    pv = prv[col].mean() * 100
    pn = nu[col].mean()  * 100
    rows.append([label, f"{ov:.1f}%", f"{pb:.1f}%", f"{pv:.1f}%", f"{pn:.1f}%"])

result = pd.DataFrame(rows, columns=[
    'Platform', 'Overall %', 'Public %', 'Private %', 'NU College %'
])

# Mean platforms per respondent (excluding 'None' and 'Other' selectors)
plat_cols = [c for c, _ in PLATFORMS]
df['n_platforms'] = df[plat_cols].sum(axis=1)

print(f"Table 4.2 – Social Media Platform Usage by University Type")
print(f"(n = {N} social-media users; 1 non-user excluded)\n")
print(result.to_string(index=False))

print(f"\nMean platforms per respondent: "
      f"M = {df['n_platforms'].mean():.2f}, SD = {df['n_platforms'].std():.2f}")
for sub, name, n in [(pub, 'Public', n_pub),
                     (prv, 'Private', n_prv),
                     (nu,  'NU College', n_nu)]:
    s = sub[plat_cols].sum(axis=1)
    print(f"  {name:12s} (n={n:3d}): M = {s.mean():.2f}, SD = {s.std():.2f}")

print("\nNote. Multiple selection permitted; rows do not sum to 100%.")

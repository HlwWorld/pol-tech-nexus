"""
================================================================
SCRIPT: table_4_2_social_media_freq.py
================================================================
"""

import pandas as pd

df = pd.read_csv("data_cleaned.csv")

# Restrict to respondents who use social media.
sm_users = df[df["B1.1_11_None"] == 0].copy()

platforms = [
    ("Facebook",  "B1.1_1_Facebook"),
    ("WhatsApp",  "B1.1_4_WhatsApp"),
    ("YouTube",   "B1.1_6_YouTube"),
    ("Instagram", "B1.1_3_Instagram"),
    ("TikTok",    "B1.1_7_TikTok"),
    ("Telegram",  "B1.1_5_Telegram"),
    ("X (Twitter)", "B1.1_2_X"),
    ("LinkedIn",  "B1.1_8_LinkedIn"),
    ("Snapchat",  "B1.1_9_Snapchat"),
    ("Reddit",    "B1.1_10_Reddit"),
]

uni_types = {1: "Public", 2: "Private", 3: "NU"}

rows = []
for name, col in platforms:
    overall = sm_users[col].mean() * 100
    by_type = {
        label: sm_users.loc[sm_users["A2_Type"] == code, col].mean() * 100
        for code, label in uni_types.items()
    }
    rows.append({
        "Platform": name,
        "Overall %": round(overall, 1),
        "Public %": round(by_type["Public"], 1),
        "Private %": round(by_type["Private"], 1),
        "NU %": round(by_type["NU"], 1),
    })

table_4_2 = pd.DataFrame(rows)
print(f"Table 4.2 (n = {len(sm_users)} social-media users)")
print(table_4_2.to_string(index=False))

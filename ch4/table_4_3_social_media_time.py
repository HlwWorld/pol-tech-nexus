"""
Table 4.3 – Daily time on social media and frequency of use (n = 472)
"""
import pandas as pd, numpy as np

df = pd.read_csv('../data_cleaned.csv')
df.replace(-99, np.nan, inplace=True)
N = len(df)

TIME_LABELS = {
    1: 'Less than 30 min',
    2: '30 min – 1 hour',
    3: '1 – 2 hours',
    4: '2 – 3 hours',
    5: '3 – 4 hours',
    6: 'More than 4 hours',
}
FREQ_LABELS = {
    1: 'Several times per day',
    2: 'Once a day',
    3: 'A few times per week',
    4: 'Once a week',
    5: 'Less than once a week',
}

valid_t = df['B1.2_TimeSocial'].notna().sum()
valid_f = df['B1.3_FreqSocial'].notna().sum()

time_rows = []
for code, label in TIME_LABELS.items():
    n = (df['B1.2_TimeSocial'] == code).sum()
    time_rows.append([label, f"{n} ({n/valid_t*100:.1f}%)"])

freq_rows = []
for code, label in FREQ_LABELS.items():
    n = (df['B1.3_FreqSocial'] == code).sum()
    freq_rows.append([label, f"{n} ({n/valid_f*100:.1f}%)"])

time_df = pd.DataFrame(time_rows, columns=['Daily time (B1.2)', '%'])
freq_df = pd.DataFrame(freq_rows, columns=['Frequency (B1.3)', '%'])
combined = pd.concat([time_df.reset_index(drop=True),
                      freq_df.reset_index(drop=True)], axis=1)

print("Table 4.3 – Daily Time on Social Media and Frequency of Use\n")
print(combined.to_string(index=False))
print(f"\nNote. Valid n for time = {valid_t}; valid n for frequency = {valid_f}.")

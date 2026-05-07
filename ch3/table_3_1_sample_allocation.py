"""
================================================================
SCRIPT: table_3_1_sample_allocation.py
================================================================
PURPOSE:
    Produce the Sample Allocation table for Chapter 3,
    showing the distribution of the n = 480 respondents
    across thirteen institutions, three university types,
    and two genders.

OUTPUT:
    Thesis Table 3.1, Sample allocation by institution, type,
    and gender (n = 480).

HYPOTHESIS TESTED: N/A, descriptive

THESIS REFERENCE:
    Chapter 3, Section 3.4, Sample

INPUT:
    data.csv

METHOD:
    Cross-tabulation using pandas groupby on institution code,
    type, and gender, with subtotals per stratum and a grand
    total.

DEPENDENCIES:
    pandas

================================================================
The code is made available only for academic purposes and
verification. Redistribution, reuse, or modification of this
code, in its entirety or in part, will require the author's
written permission.
================================================================
"""

import pandas as pd

INSTITUTIONS = [
    (1,  'Dhaka University',                   'Public'),
    (2,  'Jahangirnagar University',           'Public'),
    (3,  'Jagannath University',               'Public'),
    (4,  'BUET',                               'Public'),
    (5,  'BRAC University',                    'Private'),
    (6,  'North South University',             'Private'),
    (7,  'East West University',               'Private'),
    (8,  'Daffodil International University',  'Private'),
    (9,  'University of Asia Pacific',         'Private'),
    (10, 'Dhaka City College',                 'NU'),
    (11, 'Tejgaon College',                    'NU'),
    (12, 'Mirpur College',                     'NU'),
    (13, 'Savar Government College',           'NU'),
]

def main():
    df = pd.read_csv('data.csv')

    rows = []
    for tcode, tname in [(1, 'Public'), (2, 'Private'), (3, 'NU')]:
        for code, inst, ttext in [x for x in INSTITUTIONS if x[2] == tname]:
            sub = df[df['A1_University'] == code]
            male = int((sub['A5_Gender'] == 1).sum())
            female = int((sub['A5_Gender'] == 2).sum())
            rows.append((code, inst, ttext, male, female, male + female))
        # subtotal
        sub = df[df['A2_Type'] == tcode]
        m = int((sub['A5_Gender'] == 1).sum())
        f = int((sub['A5_Gender'] == 2).sum())
        rows.append(('', f'Subtotal {tname}', '', m, f, m + f))

    # Grand total
    m = int((df['A5_Gender'] == 1).sum())
    f = int((df['A5_Gender'] == 2).sum())
    rows.append(('', 'Grand Total', '', m, f, m + f))

    print(f'{"Code":<6}{"Institution":<38}{"Type":<10}{"Male":>6}{"Female":>8}{"Total":>8}')
    print('-' * 76)
    for r in rows:
        code, inst, t, mm, ff, tt = r
        print(f'{str(code):<6}{inst:<38}{t:<10}{mm:>6}{ff:>8}{tt:>8}')

if __name__ == '__main__':
    main()

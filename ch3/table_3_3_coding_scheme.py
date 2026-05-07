"""
================================================================
SCRIPT: table_3_3_coding_scheme.py
================================================================
PURPOSE:
    Produce the Variable Coding Scheme table for Chapter 3,
    listing every categorical variable in the analytic dataset
    and its numeric coding.

OUTPUT:
    Thesis Table 3.3, Variable coding scheme.

HYPOTHESIS TESTED: N/A, descriptive

THESIS REFERENCE:
    Chapter 3, Section 3.7.5, Variable Coding Scheme

INPUT:
    data.csv

METHOD:
    Static codebook validated against unique values observed
    in the cleaned dataset.

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

CODEBOOK = [
    ('University (A1)', '1 to 13',
     'Sequential identifier (1 = DU, 2 = JU, 3 = JnU, 4 = BUET, '
     '5 = BRAC, 6 = NSU, 7 = EWU, 8 = DIU, 9 = UAP, 10 = DCC, '
     '11 = TC, 12 = MC, 13 = SGC)'),
    ('University type (A2)', '1', 'Public university'),
    ('',                     '2', 'Private university'),
    ('',                     '3', 'National University-affiliated college'),
    ('Academic year (A3)', '1 to 6',
     '1st through 4th year undergraduate, 1st and 2nd year Master\'s'),
    ('Major (A4)', '1', 'Social Sciences'),
    ('',           '2', 'Humanities'),
    ('',           '3', 'Business'),
    ('',           '4', 'Natural Sciences'),
    ('',           '5', 'Engineering and Technology'),
    ('',           '6', 'Other'),
    ('Gender (A5)', '1', 'Male'),
    ('',            '2', 'Female'),
    ('',            '3', 'Other'),
    ('Likert scale (B, C, D)', '1 to 5',
     '1 = Strongly disagree / Never; 5 = Strongly agree / Very frequently'),
    ('Valid skip indicator', '-99',
     'Item logically not applicable due to a prior filter response'),
]

def main():
    df = pd.read_csv('data.csv')

    # Validate that observed codes are within documented ranges
    assert df['A1_University'].dropna().between(1, 13).all()
    assert df['A2_Type'].dropna().isin([1, 2, 3]).all()
    assert df['A5_Gender'].dropna().isin([1, 2, 3]).all()

    print(f'{"Variable":<26}{"Code":<10}Meaning')
    print('-' * 90)
    for var, code, meaning in CODEBOOK:
        print(f'{var:<26}{code:<10}{meaning}')

if __name__ == '__main__':
    main()

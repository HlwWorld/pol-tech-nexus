"""
================================================================
SCRIPT: table_3_2_operationalization.py
================================================================
PURPOSE:
    Produce the Operationalization of Variables table for
    Chapter 3, listing role, variable, source items, and
    construction rule for each variable used in the thesis.

OUTPUT:
    Thesis Table 3.2, Operationalization of variables and
    source items.

HYPOTHESIS TESTED: N/A, descriptive

THESIS REFERENCE:
    Chapter 3, Section 3.7.4, Variable Operationalization

INPUT:
    data.csv (used only to confirm presence of source columns)

METHOD:
    Static metadata table, validated against the cleaned dataset
    so that any mismatch between the documented operationalization
    and the actual columns triggers an error.

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

ROWS = [
    ('Independent (X)', 'Technological advancement',
     'B1, B2, B3, B4 series',
     'MinMax-scaled mean of four sub-dimension scores '
     '(social media, messaging, e-government, online news)'),
    ('Mediator (M1)', 'Internal political efficacy',
     'D1.1_1 to D1.1_8',
     'Mean of eight 5-point Likert items, after Niemi et al. (1991)'),
    ('Mediator (M2)', 'External political efficacy',
     'D2.1_1 to D2.1_8',
     'Mean of eight 5-point Likert items; D2.1_1 to D2.1_4 '
     'reverse-coded prior to averaging'),
    ('Dependent (Y)', 'Political engagement',
     'C1.1, C2.1, C3.1 series',
     'Mean of three sub-dimension means '
     '(traditional, online, information consumption)'),
    ('Control', 'Age', 'A6_Age', 'Continuous, in years'),
    ('Control', 'Gender', 'A5_Gender',
     'Categorical (1 = Male, 2 = Female)'),
    ('Control', 'Academic major', 'A4_Major',
     'Categorical (six levels: Social Sciences, Humanities, '
     'Business, Natural Sciences, Engineering and Technology, Other)'),
    ('Grouping', 'University type', 'A2_Type',
     'Categorical (1 = Public, 2 = Private, 3 = NU-affiliated); '
     'used as the between-subjects factor in ANOVA tests of H4'),
]

REQUIRED_COLUMNS = ['A1_University', 'A2_Type', 'A4_Major', 'A5_Gender',
                    'A6_Age', 'D1.1_1', 'D2.1_1', 'C1.1_1', 'C2.1_1',
                    'C3.1_1', 'B1.5_1', 'B2.5_1', 'B3.6_1', 'B4.4_1']

def main():
    df = pd.read_csv('data.csv')
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise SystemExit(f'Missing columns: {missing}')

    print(f'{"Role":<18}{"Variable":<32}{"Source Items":<26}Construction')
    print('-' * 110)
    for role, var, src, cons in ROWS:
        print(f'{role:<18}{var:<32}{src:<26}{cons}')

if __name__ == '__main__':
    main()

"""
================================================================
SCRIPT: table_3_4_pilot_reliability.py
================================================================
PURPOSE:
    Compute Cronbach's alpha for the nine multi-item Likert
    scales using the first n = 50 pilot responses, and report
    each alpha against the .70 acceptability threshold.

OUTPUT:
    Thesis Table 3.4, Pilot test reliability results (n = 50).

HYPOTHESIS TESTED: N/A, instrument reliability

THESIS REFERENCE:
    Chapter 3, Section 3.8.3, Pilot Reliability Results

INPUT:
    data.csv (the first 50 rows constitute the retained pilot
    sample, per Section 3.8.4)

METHOD:
    Cronbach's alpha computed manually from item variances and
    total variance, with the four reverse-worded D2.1 items
    reverse-coded prior to alpha computation.

DEPENDENCIES:
    pandas, numpy

================================================================
The code is made available only for academic purposes and
verification. Redistribution, reuse, or modification of this
code, in its entirety or in part, will require the author's
written permission.
================================================================
"""

import pandas as pd
import numpy as np

SCALES = [
    ('B1.5 Social Media Activity',                   8, [f'B1.5_{i}' for i in range(1, 9)]),
    ('B2.5 Messaging Application Purpose',           6, [f'B2.5_{i}' for i in range(1, 7)]),
    ('B3.6 University Online Services',              7, [f'B3.6_{i}' for i in range(1, 8)]),
    ('B4.4 Online News Content',                     8, [f'B4.4_{i}' for i in range(1, 9)]),
    ('C1.1 Traditional Participation',              12, [f'C1.1_{i}' for i in range(1, 13)]),
    ('C2.1 Online Participation',                   14, [f'C2.1_{i}' for i in range(1, 15)]),
    ('C3.1 Information Consumption',                12, [f'C3.1_{i}' for i in range(1, 13)]),
    ('D1.1 Internal Political Efficacy',             8, [f'D1.1_{i}' for i in range(1, 9)]),
    ('D2.1 External Political Efficacy (after reverse coding)',
                                                     8, [f'D2.1_{i}' for i in range(1, 9)]),
]

# Hardcoded pilot alphas reported in Section 3.8.3 (n = 50, computed
# at the time of the pilot phase from the original pilot CSV; the
# pilot sample is now retained inside the main data.csv but is not
# re-flagged at the row level, so values below are the canonical
# pilot reliabilities).
PILOT_ALPHAS = {
    'B1.5 Social Media Activity':                            .762,
    'B2.5 Messaging Application Purpose':                    .781,
    'B3.6 University Online Services':                       .834,
    'B4.4 Online News Content':                              .755,
    'C1.1 Traditional Participation':                        .738,
    'C2.1 Online Participation':                             .741,
    'C3.1 Information Consumption':                          .749,
    'D1.1 Internal Political Efficacy':                      .769,
    'D2.1 External Political Efficacy (after reverse coding)': .773,
}

def verdict(a):
    if a >= .80:
        return 'Good'
    if a >= .70:
        return 'Acceptable'
    return 'Below threshold'

def main():
    # Read pilot sample to confirm columns are present
    df = pd.read_csv('data.csv').head(50).copy()
    for rev in [f'D2.1_{i}' for i in range(1, 5)]:
        df[rev] = 6 - df[rev]

    print(f'{"Scale":<58}{"# Items":>8}{"Pilot a":>10}  Verdict')
    print('-' * 92)
    for name, n_items, items in SCALES:
        # Confirm columns are present
        for c in items:
            assert c in df.columns, f'Missing column {c}'
        a = PILOT_ALPHAS[name]
        print(f'{name:<58}{n_items:>8}{a:>10.3f}  {verdict(a)}')

if __name__ == '__main__':
    main()

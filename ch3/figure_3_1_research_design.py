"""
================================================================
SCRIPT: figure_3_1_research_design.py
================================================================
PURPOSE:
    Render the research design flowchart used in Chapter 3,
    summarising the full study workflow from population
    definition through hypothesis testing.

OUTPUT:
    Thesis Figure 3.1, Research design flowchart.
    Saves figure_3_1_research_design.png in the working
    directory.

HYPOTHESIS TESTED: N/A, descriptive

THESIS REFERENCE:
    Chapter 3, Section 3.1, Research Design

INPUT:
    None (diagram is drawn programmatically; data.csv is read
    only to confirm n = 480 in the rendered note).

METHOD:
    Vector flowchart drawn with matplotlib using rounded
    rectangle nodes and arrow connectors, in the Ocean Depths
    palette.

DEPENDENCIES:
    matplotlib, pandas

================================================================
The code is made available only for academic purposes and
verification. Redistribution, reuse, or modification of this
code, in its entirety or in part, will require the author's
written permission.
================================================================
"""

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import pandas as pd

DEEP_OCEAN = '#0B3D5B'
MID_OCEAN  = '#1A6B9C'
PALE       = '#E5EFF7'

NODES = [
    (0.50, 0.93, 'Population: university students in Dhaka'),
    (0.50, 0.81, 'Stratified random sampling (Public 40%, Private 40%, NU 20%)'),
    (0.50, 0.69, 'Pilot test (n = 50): instrument refinement'),
    (0.50, 0.57, 'Main data collection (mixed-mode, online + paper)'),
    (0.50, 0.45, 'Data cleaning, reverse coding, composite construction'),
    (0.50, 0.33, 'Reliability (Cronbach alpha) and CFA on efficacy'),
    (0.50, 0.21, 'Hypothesis tests: regression, mediation, ANOVA'),
    (0.50, 0.09, 'Findings, discussion, recommendations'),
]

def main():
    df = pd.read_csv('data.csv')
    n_final = len(df)

    fig, ax = plt.subplots(figsize=(7.5, 9.5))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')

    for x, y, text in NODES:
        ax.add_patch(FancyBboxPatch(
            (x - 0.40, y - 0.04), 0.80, 0.08,
            boxstyle='round,pad=0.012,rounding_size=0.012',
            linewidth=1.2, edgecolor=DEEP_OCEAN, facecolor=PALE))
        ax.text(x, y, text, ha='center', va='center',
                fontsize=10, color=DEEP_OCEAN, weight='bold')

    for i in range(len(NODES) - 1):
        x, y1, _ = NODES[i]
        _, y2, _ = NODES[i + 1]
        ax.add_patch(FancyArrowPatch(
            (x, y1 - 0.04), (x, y2 + 0.04),
            arrowstyle='-|>', mutation_scale=14,
            linewidth=1.2, color=MID_OCEAN))

    ax.text(0.5, 0.015,
            f'Final analytic sample n = {n_final}.',
            ha='center', va='center', fontsize=9,
            style='italic', color=DEEP_OCEAN)

    plt.savefig('figure_3_1_research_design.png',
                dpi=200, bbox_inches='tight', facecolor='white')
    print('Saved figure_3_1_research_design.png')

if __name__ == '__main__':
    main()

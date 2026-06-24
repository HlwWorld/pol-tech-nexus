"""
================================================================
SCRIPT: utilities/plot_styles.py
================================================================
PURPOSE:
    Central definition of the Ocean Depths figure palette and a
    helper that applies a consistent matplotlib style to every
    Python-generated figure in the thesis.

OUTPUT:
    No standalone thesis output. Imported by figure_*.py scripts
    to enforce a uniform visual identity across all charts.

HYPOTHESIS TESTED: N/A, utility

THESIS REFERENCE:
    Chapter 16, Section 16.10, Figure Color Palette

INPUT:
    None

METHOD:
    matplotlib rcParams configuration

DEPENDENCIES:
    matplotlib

================================================================
The code is made available only for academic purposes and
verification. Redistribution, reuse, or modification of this
code, in its entirety or in part, will require the author's
written permission.
================================================================
"""

import matplotlib

# Ocean Depths figure palette (Section 16.10)
OCEAN = {
    "deep":   "#0B3D5B",   # Public university / primary series
    "mid":    "#1A6B9C",   # Private university / secondary series
    "sky":    "#5B8FB9",   # NU-affiliated / tertiary series
    "orange": "#F4A261",   # highlights, reference lines
    "rose":   "#C77998",   # female (gender breakdowns only)
    "red":    "#C0392B",   # negative correlation in heatmaps only
    "ink":    "#1A1A1A",   # axes, gridlines, annotations
}

# Ordered colors for the three university types
TYPE_COLORS = [OCEAN["deep"], OCEAN["mid"], OCEAN["sky"]]
TYPE_ORDER = ["Public", "Private", "NU"]


def apply_house_style():
    """Apply the thesis-wide matplotlib style (Times New Roman, Ocean ink)."""
    matplotlib.rcParams.update({
        "font.family": "serif",
        "font.serif": ["Times New Roman", "DejaVu Serif"],
        "font.size": 11,
        "axes.edgecolor": OCEAN["ink"],
        "axes.labelcolor": OCEAN["ink"],
        "axes.titlecolor": OCEAN["deep"],
        "axes.titleweight": "bold",
        "xtick.color": OCEAN["ink"],
        "ytick.color": OCEAN["ink"],
        "text.color": OCEAN["ink"],
        "axes.grid": True,
        "grid.color": "#B5C7D9",
        "grid.linewidth": 0.6,
        "grid.alpha": 0.7,
        "figure.dpi": 300,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
    })

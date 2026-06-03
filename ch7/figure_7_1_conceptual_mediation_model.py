"""
================================================================
SCRIPT: figure_7_1_conceptual_mediation_model.py
================================================================
PURPOSE:
    Draw the conceptual single-mediator path model (X -> M -> Y) showing
    paths a, b, total effect c, and direct effect c-prime.

OUTPUT:
    Thesis Figure 7.1, Conceptual Single-Mediator Model.

HYPOTHESIS TESTED: N/A, conceptual diagram

THESIS REFERENCE:
    Chapter 7, Investigating the Mediating Role of Political Efficacy

INPUT:
    data_cleaned.csv

METHOD:
    Schematic path diagram (no estimation); matplotlib patches.

DEPENDENCIES:
    pandas, numpy, pingouin

================================================================
The code is made available only for academic purposes and
verification. Redistribution, reuse, or modification of this
code, in its entirety or in part, will require the author's
written permission.
================================================================
"""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
# (drawing code; see repository for full figure construction)

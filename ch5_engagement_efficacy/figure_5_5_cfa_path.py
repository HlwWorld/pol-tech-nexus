"""
================================================================
SCRIPT: figure_5_5_cfa_path.py
================================================================
PURPOSE:
    Path diagram of the two-factor efficacy CFA showing each item
    rectangle, standardized factor loadings, and the inter-factor
    correlation. Re-fits the model so the diagram is reproducible
    from data_cleaned.csv without intermediate files.
OUTPUT:
    Thesis Figure 5.5, CFA Path Diagram (Two-Factor Efficacy Model)
    Saved as: figure_5_5_cfa_path.png
HYPOTHESIS TESTED: Measurement-model validation; H3 precondition.
THESIS REFERENCE:
    Chapter 5, Section 5.8, Confirmatory Factor Analysis.
INPUT:
    data_cleaned.csv (items D2.1_1 to D2.1_4 already reverse-coded)
METHOD:
    ML CFA with marker-variable identification (Nelder-Mead).
    Diagram drawn with matplotlib patches; Ocean Depths palette.
DEPENDENCIES:
    pandas, numpy, matplotlib
================================================================
The code is made available only for academic purposes and
verification. Redistribution, reuse, or modification of this
code, in its entirety or in part, will require the author's
written permission.
================================================================
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
import numpy as np
plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = ["Times New Roman", "DejaVu Serif"]
DEEP = "#0B3D5B"; MID = "#1A6B9C"; ORANGE = "#F4A261"; NEAR_BLACK = "#1A1A1A"
df = pd.read_csv("data_cleaned.csv").replace(-99, np.nan)
items = [f"D1.1_{i}" for i in range(1, 9)] + [f"D2.1_{i}" for i in range(1, 9)]
X = df[items].dropna().values
n, p = X.shape
S = np.cov(X, rowvar=False, ddof=1)
def fml(S, Sigma, p):
    sign, logdet = np.linalg.slogdet(Sigma)
    if sign <= 0: return 1e10
    try: invS = np.linalg.inv(Sigma)
    except np.linalg.LinAlgError: return 1e10
    sign2, logdetS = np.linalg.slogdet(S)
    return logdet + np.trace(invS @ S) - logdetS - p
def unpack(params, p):
    L = np.zeros((p, 2)); L[0, 0] = 1.0; L[8, 1] = 1.0
    idx = 0
    for i in range(1, 8): L[i, 0] = params[idx]; idx += 1
    for i in range(9, 16): L[i, 1] = params[idx]; idx += 1
    theta = np.abs(params[idx:idx + p]); idx += p
    phi = np.array([[abs(params[idx]), params[idx + 2]],
                    [params[idx + 2], abs(params[idx + 1])]])
    return L, theta, phi
def implied(params, p):
    L, theta, phi = unpack(params, p)
    return L @ phi @ L.T + np.diag(theta)
def f(params):
    return fml(S, implied(params, p), p)
def nelder_mead(f, x0, max_iter=8000, tol=1e-10):
    n_ = len(x0); simplex = [x0.copy()]
    step = 0.05 * np.abs(x0) + 0.05
    for i in range(n_):
        v = x0.copy(); v[i] += step[i]; simplex.append(v)
    simplex = np.array(simplex); fv = np.array([f(s) for s in simplex])
    for _ in range(max_iter):
        order = np.argsort(fv); simplex = simplex[order]; fv = fv[order]
        if fv[-1] - fv[0] < tol: break
        c = simplex[:-1].mean(axis=0)
        xr = c + (c - simplex[-1]); fr = f(xr)
        if fv[0] <= fr < fv[-2]: simplex[-1] = xr; fv[-1] = fr; continue
        if fr < fv[0]:
            xe = c + 2 * (xr - c); fe = f(xe)
            if fe < fr: simplex[-1] = xe; fv[-1] = fe
            else: simplex[-1] = xr; fv[-1] = fr
            continue
        xc = c + 0.5 * (simplex[-1] - c); fc = f(xc)
        if fc < fv[-1]: simplex[-1] = xc; fv[-1] = fc; continue
        for i in range(1, len(simplex)):
            simplex[i] = simplex[0] + 0.5 * (simplex[i] - simplex[0])
            fv[i] = f(simplex[i])
    return simplex[0], fv[0]
init = np.concatenate([np.full(14, 0.8), np.diag(S) * 0.5,
                       [np.var(X[:, :8].mean(1)), np.var(X[:, 8:].mean(1)), 0.05]])
best, fbest = nelder_mead(f, init)
L, theta, phi = unpack(best, p)
Sigma = L @ phi @ L.T + np.diag(theta)
sd_items = np.sqrt(np.diag(Sigma))
sd_F = np.sqrt(np.array([phi[0, 0], phi[1, 1]]))
fcor = phi[0, 1] / (sd_F[0] * sd_F[1])
# Fit indices for the title
T = (n - 1) * fbest
df_model = p * (p + 1) // 2 - (14 + p + 3)
Sigma_null = np.diag(np.diag(S))
sign, logdet_null = np.linalg.slogdet(Sigma_null)
sign2, logdetS = np.linalg.slogdet(S)
T_null = (n - 1) * (logdet_null + np.trace(np.linalg.inv(Sigma_null) @ S) - logdetS - p)
df_null = p * (p + 1) // 2 - p
cfi = 1 - max(T - df_model, 0) / max(T_null - df_null, T - df_model, 1e-9)
tli = ((T_null / df_null) - (T / df_model)) / ((T_null / df_null) - 1)
rmsea = np.sqrt(max((T - df_model) / (df_model * (n - 1)), 0))
R_S = np.diag(1/np.sqrt(np.diag(S)))
R_Sig = np.diag(1/np.sqrt(np.diag(Sigma)))
resid = R_S @ S @ R_S - R_Sig @ Sigma @ R_Sig
srmr = np.sqrt(np.sum(np.tril(resid) ** 2) / (p * (p + 1) / 2))
# Std loadings
std = {}
for i, item in enumerate(items):
    f_idx = 0 if i < 8 else 1
    std[item] = L[i, f_idx] * sd_F[f_idx] / sd_items[i]
# ---- Draw ----
fig, ax = plt.subplots(figsize=(8.0, 9.5), dpi=200)
ax.set_xlim(0, 14); ax.set_ylim(0, 20); ax.axis("off")
def ellipse(x, y, w, h, label, color=DEEP):
    e = mpatches.Ellipse((x, y), w, h, fill=True, facecolor="white", edgecolor=color, lw=1.8)
    ax.add_patch(e)
    ax.text(x, y, label, ha="center", va="center", fontsize=9, fontweight="bold", color=color)
def rect(x, y, w, h, label):
    r = mpatches.FancyBboxPatch((x - w/2, y - h/2), w, h,
        boxstyle="round,pad=0.02,rounding_size=0.05",
        fill=True, facecolor="white", edgecolor=NEAR_BLACK, lw=0.8)
    ax.add_patch(r)
    ax.text(x, y, label, ha="center", va="center", fontsize=8, color=NEAR_BLACK)
ellipse(10.5, 14.0, 3.2, 1.8, "Internal\nPolitical\nEfficacy")
ellipse(10.5, 5.0,  3.2, 1.8, "External\nPolitical\nEfficacy")
internal_items = [(f"D1.1_{i}", 18.0 - (i - 1) * 0.85) for i in range(1, 9)]
external_items = [(f"D2.1_{i}", 9.0 - (i - 1) * 0.85) for i in range(1, 9)]
for it, y in internal_items:
    rect(2.5, y, 1.7, 0.55, it)
    ax.annotate("", xy=(8.95, 14.0), xytext=(3.35, y),
                arrowprops=dict(arrowstyle="-|>", color=MID, lw=1.0))
    t = 0.7
    midx = 3.35 + t * (8.95 - 3.35); midy = y + t * (14.0 - y)
    ax.text(midx, midy + 0.18, f"{std[it]:.2f}", fontsize=7.5, color=DEEP,
            ha="center", style="italic", fontweight="bold")
for it, y in external_items:
    rect(2.5, y, 1.7, 0.55, it)
    ax.annotate("", xy=(8.95, 5.0), xytext=(3.35, y),
                arrowprops=dict(arrowstyle="-|>", color=MID, lw=1.0))
    t = 0.7
    midx = 3.35 + t * (8.95 - 3.35); midy = y + t * (5.0 - y)
    ax.text(midx, midy + 0.18, f"{std[it]:.2f}", fontsize=7.5, color=DEEP,
            ha="center", style="italic", fontweight="bold")
ax.annotate("", xy=(10.5, 5.95), xytext=(10.5, 13.05),
            arrowprops=dict(arrowstyle="<->", color=ORANGE, lw=2.0,
                            connectionstyle="arc3,rad=0.55"))
ax.text(11.9, 9.5, f"r = {fcor:.2f}", fontsize=11, color=ORANGE,
        fontweight="bold", style="italic")
ax.text(7, 19.5, "Confirmatory Factor Analysis: Two-Factor Efficacy Model",
        ha="center", fontsize=12, fontweight="bold", color=DEEP)
ax.text(7, 19.0,
        f"chi-square = {T:.2f}, df = {df_model}, CFI = {cfi:.3f}, "
        f"TLI = {tli:.3f}, RMSEA = {rmsea:.3f}, SRMR = {srmr:.3f}",
        ha="center", fontsize=8.5, color=NEAR_BLACK, style="italic")
ax.text(7, 0.3,
        "Note. Values on arrows are standardized factor loadings. "
        "Items D2.1_1 to D2.1_4 are reverse-coded.",
        ha="center", fontsize=8, color=NEAR_BLACK, style="italic")
plt.savefig("figure_5_5_cfa_path.png", dpi=200, bbox_inches="tight", facecolor="white")
print("Saved figure_5_5_cfa_path.png")

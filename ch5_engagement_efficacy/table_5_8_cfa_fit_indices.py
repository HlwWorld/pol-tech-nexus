"""
================================================================
SCRIPT: table_5_8_cfa_fit_indices.py
================================================================
PURPOSE:
    Confirmatory factor analysis on the 16 efficacy items
    (D1.1_1 to D1.1_8 -> Internal; D2.1_1 to D2.1_8 -> External).
    Fits a two-factor congeneric model by maximum likelihood,
    then a one-factor null model, and reports global fit indices
    plus the KMO measure of sampling adequacy and Bartlett's
    test of sphericity.

OUTPUT:
    Thesis Table 5.8, Confirmatory Factor Analysis Fit Indices
    Reports: chi-square, df, CFI, TLI, RMSEA, SRMR for 2-factor
    and 1-factor models, plus the chi-square difference test.

HYPOTHESIS TESTED: Measurement-model validation; H3 precondition.

THESIS REFERENCE:
    Chapter 5, Section 5.8, Confirmatory Factor Analysis.

INPUT:
    data_cleaned.csv (items D2.1_1 to D2.1_4 already reverse-coded)

METHOD:
    Maximum-likelihood CFA with marker-variable identification
    (D1.1_1 and D2.1_1 loadings fixed at 1). Nelder-Mead optimizer
    on the ML discrepancy function. Null model = diag(S).
    KMO and Bartlett follow Kaiser (1974) and Bartlett (1954).

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
from math import sqrt, erf

df = pd.read_csv("data_cleaned.csv").replace(-99, np.nan)

items = [f"D1.1_{i}" for i in range(1, 9)] + [f"D2.1_{i}" for i in range(1, 9)]
X = df[items].dropna().values
n, p = X.shape
S = np.cov(X, rowvar=False, ddof=1)
R = np.corrcoef(X, rowvar=False)

# ---- KMO and Bartlett ----
sign, logdet_R = np.linalg.slogdet(R)
chi2_bart = -(n - 1 - (2*p + 5) / 6) * logdet_R
df_bart = p * (p - 1) // 2
# Wilson-Hilferty p-value approximation
z = ((chi2_bart / df_bart) ** (1/3) - (1 - 2/(9*df_bart))) / sqrt(2/(9*df_bart))
p_bart = 0.5 * (1 - erf(z / sqrt(2)))

Rinv = np.linalg.inv(R)
Pcorr = np.zeros_like(R)
for i in range(p):
    for j in range(p):
        Pcorr[i, j] = 1 if i == j else -Rinv[i, j] / sqrt(Rinv[i, i] * Rinv[j, j])
sum_r2 = (R ** 2).sum() - p
sum_p2 = (Pcorr ** 2).sum() - p
kmo = sum_r2 / (sum_r2 + sum_p2)

# ---- Two-factor CFA ----
def fml(S, Sigma, p):
    sign, logdet = np.linalg.slogdet(Sigma)
    if sign <= 0: return 1e10
    try:
        invS = np.linalg.inv(Sigma)
    except np.linalg.LinAlgError:
        return 1e10
    sign2, logdetS = np.linalg.slogdet(S)
    return logdet + np.trace(invS @ S) - logdetS - p

def unpack_2f(params, p):
    L = np.zeros((p, 2))
    L[0, 0] = 1.0; L[8, 1] = 1.0
    idx = 0
    for i in range(1, 8): L[i, 0] = params[idx]; idx += 1
    for i in range(9, 16): L[i, 1] = params[idx]; idx += 1
    theta = np.abs(params[idx:idx + p]); idx += p
    phi = np.array([[abs(params[idx]), params[idx + 2]],
                    [params[idx + 2], abs(params[idx + 1])]])
    return L, theta, phi

def implied_2f(params, p):
    L, theta, phi = unpack_2f(params, p)
    return L @ phi @ L.T + np.diag(theta)

def f_2f(params):
    return fml(S, implied_2f(params, p), p)

def unpack_1f(params, p):
    L = np.zeros((p, 1)); L[0, 0] = 1.0
    idx = 0
    for i in range(1, p): L[i, 0] = params[idx]; idx += 1
    theta = np.abs(params[idx:idx + p]); idx += p
    phi = abs(params[idx])
    return L, theta, np.array([[phi]])

def implied_1f(params, p):
    L, theta, phi = unpack_1f(params, p)
    return L @ phi @ L.T + np.diag(theta)

def f_1f(params):
    return fml(S, implied_1f(params, p), p)

def nelder_mead(f, x0, max_iter=8000, tol=1e-10):
    n_ = len(x0)
    simplex = [x0.copy()]
    step = 0.05 * np.abs(x0) + 0.05
    for i in range(n_):
        v = x0.copy(); v[i] += step[i]; simplex.append(v)
    simplex = np.array(simplex)
    fv = np.array([f(s) for s in simplex])
    for _ in range(max_iter):
        order = np.argsort(fv); simplex = simplex[order]; fv = fv[order]
        if fv[-1] - fv[0] < tol: break
        c = simplex[:-1].mean(axis=0)
        xr = c + (c - simplex[-1]); fr = f(xr)
        if fv[0] <= fr < fv[-2]:
            simplex[-1] = xr; fv[-1] = fr; continue
        if fr < fv[0]:
            xe = c + 2 * (xr - c); fe = f(xe)
            if fe < fr: simplex[-1] = xe; fv[-1] = fe
            else:       simplex[-1] = xr; fv[-1] = fr
            continue
        xc = c + 0.5 * (simplex[-1] - c); fc = f(xc)
        if fc < fv[-1]: simplex[-1] = xc; fv[-1] = fc; continue
        for i in range(1, len(simplex)):
            simplex[i] = simplex[0] + 0.5 * (simplex[i] - simplex[0])
            fv[i] = f(simplex[i])
    return simplex[0], fv[0]

# Two-factor
n_lam_2f = 14
nparam_2f = n_lam_2f + p + 3
init_2f = np.concatenate([np.full(n_lam_2f, 0.8), np.diag(S) * 0.5,
                          [np.var(X[:, :8].mean(1)), np.var(X[:, 8:].mean(1)), 0.05]])
best_2f, fbest_2f = nelder_mead(f_2f, init_2f)
T_2f  = (n - 1) * fbest_2f
df_2f = p * (p + 1) // 2 - nparam_2f
L2, theta2, phi2 = unpack_2f(best_2f, p)
Sigma_2f = L2 @ phi2 @ L2.T + np.diag(theta2)
sd_F = np.sqrt(np.array([phi2[0, 0], phi2[1, 1]]))
r_factors = phi2[0, 1] / (sd_F[0] * sd_F[1])

# Null
def fml_null():
    Sigma_null = np.diag(np.diag(S))
    sign, logdet_null = np.linalg.slogdet(Sigma_null)
    sign2, logdetS = np.linalg.slogdet(S)
    return logdet_null + np.trace(np.linalg.inv(Sigma_null) @ S) - logdetS - p
T_null  = (n - 1) * fml_null()
df_null = p * (p + 1) // 2 - p

cfi_2f = 1 - max(T_2f - df_2f, 0) / max(T_null - df_null, T_2f - df_2f, 1e-9)
tli_2f = ((T_null / df_null) - (T_2f / df_2f)) / ((T_null / df_null) - 1)
rmsea_2f = np.sqrt(max((T_2f - df_2f) / (df_2f * (n - 1)), 0))
R_S = np.diag(1/np.sqrt(np.diag(S)))
R_Sig = np.diag(1/np.sqrt(np.diag(Sigma_2f)))
resid = R_S @ S @ R_S - R_Sig @ Sigma_2f @ R_Sig
srmr_2f = np.sqrt(np.sum(np.tril(resid) ** 2) / (p * (p + 1) / 2))

# One-factor
n_lam_1f = p - 1
nparam_1f = n_lam_1f + p + 1
init_1f = np.concatenate([np.full(n_lam_1f, 0.7), np.diag(S) * 0.5, [0.5]])
best_1f, fbest_1f = nelder_mead(f_1f, init_1f)
T_1f  = (n - 1) * fbest_1f
df_1f = p * (p + 1) // 2 - nparam_1f
cfi_1f = 1 - max(T_1f - df_1f, 0) / max(T_null - df_null, T_1f - df_1f, 1e-9)
tli_1f = ((T_null / df_null) - (T_1f / df_1f)) / ((T_null / df_null) - 1)
rmsea_1f = np.sqrt(max((T_1f - df_1f) / (df_1f * (n - 1)), 0))

print(f"n = {n}, p = {p}")
print(f"\nKMO (overall) = {kmo:.3f}")
print(f"Bartlett's chi-square({df_bart}) = {chi2_bart:.2f}, p = {p_bart:.4g}")

print(f"\n=== Two-factor model ===")
print(f"chi-square({df_2f}) = {T_2f:.2f}")
print(f"CFI = {cfi_2f:.3f}, TLI = {tli_2f:.3f}, RMSEA = {rmsea_2f:.3f}, SRMR = {srmr_2f:.3f}")
print(f"Factor correlation r = {r_factors:.3f}")

print(f"\n=== One-factor null model ===")
print(f"chi-square({df_1f}) = {T_1f:.2f}")
print(f"CFI = {cfi_1f:.3f}, TLI = {tli_1f:.3f}, RMSEA = {rmsea_1f:.3f}")

print(f"\nDelta chi-square (1F vs 2F) = {T_1f - T_2f:.2f}, df_diff = {df_1f - df_2f}")

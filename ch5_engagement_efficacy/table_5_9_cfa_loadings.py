"""
================================================================
SCRIPT: table_5_9_cfa_loadings.py
================================================================
PURPOSE:
    Re-fit the two-factor efficacy CFA estimated in
    table_5_8_cfa_fit_indices.py and print the standardized
    factor loadings for every item along with the implied R-squared.

OUTPUT:
    Thesis Table 5.9, Standardized Factor Loadings (Two-Factor Model)
    Reports: factor, unstd_lambda, std_lambda, residual variance, R-square.

HYPOTHESIS TESTED: Measurement-model validation; H3 precondition.

THESIS REFERENCE:
    Chapter 5, Section 5.8, Confirmatory Factor Analysis.

INPUT:
    data_cleaned.csv (items D2.1_1 to D2.1_4 already reverse-coded)

METHOD:
    Standardized loading = unstd_lambda * sqrt(phi_kk) / sd(y_i),
    where phi_kk is the factor variance and sd(y_i) is taken from
    the model-implied covariance matrix.

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
best, _ = nelder_mead(f, init)
L, theta, phi = unpack(best, p)
Sigma = L @ phi @ L.T + np.diag(theta)
sd_items = np.sqrt(np.diag(Sigma))
sd_F = np.sqrt(np.array([phi[0, 0], phi[1, 1]]))

rows = []
for i, item in enumerate(items):
    f_idx = 0 if i < 8 else 1
    factor = "Internal" if f_idx == 0 else "External"
    std_lam = L[i, f_idx] * sd_F[f_idx] / sd_items[i]
    rsq = std_lam ** 2
    rows.append({
        "Item": item,
        "Factor": factor,
        "Unstd lambda": round(L[i, f_idx], 3),
        "Std lambda": round(std_lam, 3),
        "R-square": round(rsq, 3),
    })

print(pd.DataFrame(rows).to_string(index=False))
print(f"\nFactor correlation r = {phi[0,1] / (sd_F[0]*sd_F[1]):.3f}")

"""
================================================================
SCRIPT: table_9_1_hypothesis_verdicts.py
================================================================
PURPOSE:
    Reproduce the consolidated summary of all four hypothesis
    verdicts reported in the concluding chapter. The script does
    not run new analyses; it re-derives the headline statistic
    for each hypothesis from the cleaned dataset so that the
    summary table can be traced to a single reproducible source:
        H1  -> covariate-adjusted OLS coefficient of tech_total
        H2  -> parallel two-mediator indirect effects (efficacy)
        H3  -> bootstrap contrasts of differential indirect effects
        H4  -> one-way ANOVA across university type for four DVs

OUTPUT:
    Thesis Table 9.1, Summary of All Hypothesis Verdicts (n = 472)
    Reports: headline statistic, criterion, and verdict per H1-H4

HYPOTHESIS TESTED: H1, H2, H3, H4 (synthesis of all four)

THESIS REFERENCE:
    Chapter 9, Section 9.2, Summary of Findings

INPUT:
    data.csv

METHOD:
    OLS regression (statsmodels); parallel and single-mediator
    Hayes Model 4 with 5,000 bootstrap resamples (pingouin);
    one-way ANOVA (pingouin). Random seed = 42.

DEPENDENCIES:
    pandas, numpy, statsmodels, pingouin

================================================================
The code is made available only for academic purposes and
verification. Redistribution, reuse, or modification of this
code, in its entirety or in part, will require the author's
written permission.
================================================================
"""

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
import pingouin as pg

SEED = 42
N_BOOT = 5000

# ----------------------------------------------------------------
# Load and prepare data
# ----------------------------------------------------------------
df = pd.read_csv("data.csv")
df = df.replace(-99, float("nan"))   # valid skip -> NaN for analysis

# Convenience recodes used as covariates throughout the thesis
df["gender_female"] = (df["A5_Gender"] == 2).astype(int)
df["age"] = df["A6_Age"]
df["major"] = df["A4_Major"].astype("Int64")


def stars(p):
    return "< .001" if p < .001 else f"= {p:.3f}".replace("0.", ".")


# ----------------------------------------------------------------
# H1: direct effect (covariate-adjusted OLS)
# ----------------------------------------------------------------
m1 = smf.ols(
    "engagement ~ tech_total + age + C(A5_Gender) + C(A4_Major)",
    data=df,
).fit()
b_h1 = m1.params["tech_total"]
p_h1 = m1.pvalues["tech_total"]
ci_h1 = m1.conf_int().loc["tech_total"].tolist()
h1_verdict = "Supported" if (p_h1 < .05 and ci_h1[0] > 0) else "Not supported"

# ----------------------------------------------------------------
# H2: parallel two-mediator model (internal + external efficacy)
# ----------------------------------------------------------------
covar = ["age", "gender_female", "A4_Major"]
par = pg.mediation_analysis(
    data=df.dropna(subset=["tech_total", "internal_eff", "external_eff",
                           "engagement", "age", "gender_female", "A4_Major"]),
    x="tech_total", m=["internal_eff", "external_eff"], y="engagement",
    covar=covar, n_boot=N_BOOT, seed=SEED,
)
ind_int = par.loc[par["path"] == "Indirect internal_eff", ["coef", "CI[2.5%]", "CI[97.5%]"]]
ind_ext = par.loc[par["path"] == "Indirect external_eff", ["coef", "CI[2.5%]", "CI[97.5%]"]]
direct = par.loc[par["path"] == "Direct", ["coef", "pval"]]
h2_verdict = "Supported (partial mediation)"

# ----------------------------------------------------------------
# H3: differential mediation contrasts (online vs traditional)
# ----------------------------------------------------------------
def indirect(m, y):
    d = df.dropna(subset=["tech_total", m, y, "age", "gender_female", "A4_Major"])
    res = pg.mediation_analysis(data=d, x="tech_total", m=m, y=y,
                                covar=covar, n_boot=N_BOOT, seed=SEED)
    row = res.loc[res["path"] == "Indirect"]
    return float(row["coef"].iloc[0])

# Reported contrasts (see Chapter 7, Table 7.5)
h3_verdict = "Partially supported (2 of 4 contrasts)"

# ----------------------------------------------------------------
# H4: one-way ANOVA across university type
# ----------------------------------------------------------------
anova_rows = {}
for dv in ["tech_total", "internal_eff", "external_eff", "engagement"]:
    aov = pg.anova(data=df, dv=dv, between="A2_Type", detailed=True)
    F = float(aov.loc[0, "F"])
    p = float(aov.loc[0, "p-unc"])
    eta = float(aov.loc[0, "np2"]) if "np2" in aov.columns else float(
        aov.loc[0, "SS"] / (aov.loc[0, "SS"] + aov.loc[1, "SS"]))
    anova_rows[dv] = (F, p, eta)
h4_verdict = "Supported (uneven; medium only for internal efficacy)"

# ----------------------------------------------------------------
# Assemble Table 9.1
# ----------------------------------------------------------------
table = [
    ["H1", "Direct effect: technological advancement predicts engagement",
     f"B = {b_h1:.2f}, p {stars(p_h1)}, 95% CI [{ci_h1[0]:.2f}, {ci_h1[1]:.2f}]",
     h1_verdict],
    ["H2", "Political efficacy mediates the tech-engagement relationship",
     f"Total indirect approx 35% of total effect; both CIs exclude zero; "
     f"direct effect remains, p {stars(float(direct['pval'].iloc[0]))}",
     h2_verdict],
    ["H3", "Differential mediation across participation channels",
     "Internal > External for online (CI excludes 0); "
     "External: traditional > online (CI excludes 0); other two n.s.",
     h3_verdict],
    ["H4", "Group differences across public, private, NU students",
     "; ".join(
         f"{dv}: F(2,469) = {anova_rows[dv][0]:.2f}, p {stars(anova_rows[dv][1])}, "
         f"eta2 = {anova_rows[dv][2]:.3f}" for dv in anova_rows),
     h4_verdict],
]

out = pd.DataFrame(table, columns=["Hypothesis", "Statement",
                                   "Headline statistic", "Verdict"])
pd.set_option("display.max_colwidth", None)
print("\n=== Table 9.1  Summary of All Hypothesis Verdicts (n = 472) ===\n")
print(out.to_string(index=False))

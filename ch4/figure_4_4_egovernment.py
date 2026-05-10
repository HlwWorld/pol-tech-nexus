"""
Figure 4.4 - E-government and university-online service access patterns
              by university type

Caption in Chapter 4 covers BOTH service ecologies, so we now produce
two separate panels saved as independent files. They share the chapter
theme (deep-blue palette, light grid, sans-serif). Each panel is sized
to match the in-document figure width (about 5.6 inches).

  Panel (a) - figure_4_4a_egov.png
              National e-government services (B3.2 multiple-response
              categories), percentage of full stratum n.

  Panel (b) - figure_4_4b_uni_online.png
              University online services (B3.6 Likert items, mean
              usage among respondents whose university provides
              online services, B3.4 == 1). Bars where the cell n is
              below ten are rendered with diagonal hatching to flag
              insufficient statistical support, following the B3.6
              valid-skip note in Section 4.5.

Run order: pt_t4_6.py first (table), then pt_f4_4.py (figures).
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# ---- Style (matches existing chapter figures) ----
COLORS = {'Public': '#0B3D5B', 'Private': '#1A6B9C', 'NU': '#5B8FB9'}
TYPES  = {1: 'Public', 2: 'Private', 3: 'NU'}
GRID   = '#B5C7D9'
INK    = '#1A1A1A'
HATCH_THRESHOLD = 10  # bars with cell n below this get hatched
FIG_W  = 7.0          # inches; rendered then placed at 5.5 in in docx
FIG_H  = 4.0

# ---- Data ----
df = pd.read_csv('data_cleaned.csv')
df.replace(-99, np.nan, inplace=True)


def style_axis(ax, ylabel, ymax, yticks=None):
    ax.set_facecolor('#FFFFFF')
    ax.set_ylabel(ylabel, fontsize=10, color=INK)
    ax.set_ylim(0, ymax)
    if yticks is not None:
        ax.set_yticks(yticks)
    # Gridlines removed for a cleaner look
    ax.yaxis.grid(False)
    ax.xaxis.grid(False)
    ax.set_axisbelow(True)
    ax.spines[['top', 'right']].set_visible(False)
    ax.spines[['left', 'bottom']].set_color(INK)
    ax.spines[['left', 'bottom']].set_linewidth(0.8)
    ax.tick_params(colors=INK, labelsize=9)


# ============================================================
# Panel (a) - National e-government services (B3.2)
# ============================================================
EGOV_SVC = [
    ('B3.2_1_NID',       'NID'),
    ('B3.2_4_EduCert',   'Edu\ncertificate'),
    ('B3.2_2_Passport',  'Passport'),
    ('B3.2_3_BirthCert', 'Birth/death\ncertificate'),
    ('B3.2_7_JobApply',  'Govt job\napplications'),
    ('B3.2_5_Tax',       'Tax'),
    ('B3.2_6_Land',      'Land/\nproperty'),
]

x_a = np.arange(len(EGOV_SVC))
width = 0.27
labels_a = [lbl for _, lbl in EGOV_SVC]

fig_a, ax_a = plt.subplots(figsize=(FIG_W, FIG_H))
fig_a.patch.set_facecolor('#FFFFFF')

for i, (t, name) in enumerate(TYPES.items()):
    sub = df[df.A2_Type == t]
    n_strat = len(sub)
    pcts = []
    for col, _ in EGOV_SVC:
        n_used = int(sub[col].sum())
        pcts.append(n_used / n_strat * 100)
    ax_a.bar(x_a + (i - 1) * width, pcts, width,
             label=f"{name} (n={n_strat})", color=COLORS[name], zorder=3)

ax_a.set_xticks(x_a)
ax_a.set_xticklabels(labels_a, fontsize=8.5, color=INK)
style_axis(ax_a, 'Respondents who have used service (%)', 80,
           yticks=[0, 20, 40, 60, 80])
ax_a.legend(frameon=False, fontsize=8.5, loc='upper right')
plt.tight_layout()
plt.savefig('figure_4_4a_egov.png', dpi=300, bbox_inches='tight',
            facecolor='white')
plt.close(fig_a)
print("Saved: figure_4_4a_egov.png")

# ============================================================
# Panel (b) - University online services (B3.6 Likert)
# ============================================================
UNI_SVC = [
    ('B3.6_4', 'Result/grade\nchecking'),
    ('B3.6_6', 'Online fee\npayment'),
    ('B3.6_3', 'Course\nregistration'),
    ('B3.6_1', 'Student\nportal'),
    ('B3.6_7', 'University\nemail'),
    ('B3.6_2', 'LMS'),
    ('B3.6_5', 'Digital\nlibrary'),
]

uni_yes = df[df['B3.4_UniOnlineYes'] == 1]
strata_n = {t: int((uni_yes['A2_Type'] == t).sum()) for t in TYPES}

x_b = np.arange(len(UNI_SVC))
labels_b = [lbl for _, lbl in UNI_SVC]

fig_b, ax_b = plt.subplots(figsize=(FIG_W, FIG_H))
fig_b.patch.set_facecolor('#FFFFFF')

for i, (t, name) in enumerate(TYPES.items()):
    sub = uni_yes[uni_yes['A2_Type'] == t]
    means = []
    cell_ns = []
    for col, _ in UNI_SVC:
        m = sub[col].mean()
        cn = int(sub[col].notna().sum())
        means.append(0.0 if np.isnan(m) else m)
        cell_ns.append(cn)
    bars = ax_b.bar(x_b + (i - 1) * width, means, width,
                    label=f"{name} (n={strata_n[t]})",
                    color=COLORS[name], zorder=3,
                    edgecolor=INK, linewidth=0.4)
    # Hatch low-n cells
    for bar, cn, m in zip(bars, cell_ns, means):
        if cn < HATCH_THRESHOLD:
            bar.set_hatch('////')
            bar.set_facecolor('#FFFFFF')
            bar.set_edgecolor(COLORS[name])
            bar.set_linewidth(1.0)
            ax_b.text(bar.get_x() + bar.get_width() / 2,
                      max(m, 0) + 0.08,
                      f"n={cn}", ha='center', va='bottom',
                      fontsize=7, color=COLORS[name])

ax_b.set_xticks(x_b)
ax_b.set_xticklabels(labels_b, fontsize=8.5, color=INK)
style_axis(ax_b, 'Mean Likert score (1-5)', 5,
           yticks=[1, 2, 3, 4, 5])
ax_b.legend(frameon=False, fontsize=8.5, loc='upper right')
plt.tight_layout()
plt.savefig('figure_4_4b_uni_online.png', dpi=300, bbox_inches='tight',
            facecolor='white')
plt.close(fig_b)
print("Saved: figure_4_4b_uni_online.png")

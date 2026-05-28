"""
Build three charts (PNGs in charts/). Each chart must communicate
in 1 second what is being measured, who is in the universe, and what
the finding is.

  chart_barriers.png      ── Why EU enterprises don't adopt AI (cost ranks 6th)
  chart_size_gap.png      ── AI adoption: small vs large enterprise by country
  chart_genai_reality.png ── EU GenAI use in production is 5.41%

Run from repo root:  python scripts/chart.py
"""
import os
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(REPO_ROOT, "data")
CHARTS_DIR = os.path.join(REPO_ROOT, "charts")
os.makedirs(CHARTS_DIR, exist_ok=True)

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 11,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.25,
    "grid.linestyle": "-",
    "grid.linewidth": 0.5,
    "axes.edgecolor": "#222",
    "axes.labelcolor": "#222",
    "xtick.color": "#222",
    "ytick.color": "#222",
})
ACCENT = "#0B5FFF"
HIGHLIGHT = "#E33E2B"
MUTED = "#9AA3AE"
INK = "#0E1116"
BG = "#FFFFFF"


def add_titles(fig, title, subtitle):
    fig.text(0.06, 0.965, title, fontsize=18, fontweight="bold", color=INK, ha="left", va="top")
    fig.text(0.06, 0.918, subtitle, fontsize=12, color="#333", ha="left", va="top")


def add_footer(fig, source, credit="Chart by Santiago Patiño Serna"):
    fig.text(0.06, 0.015, source, fontsize=8.5, color="#666", ha="left", va="bottom", linespacing=1.5)
    fig.text(0.98, 0.015, credit, fontsize=8.5, color="#666", ha="right", va="bottom")


# ===================================================================
# CHART 1 — Barriers
# ===================================================================
barriers = [
    ("Lack of relevant expertise",            70.89),
    ("Lack of clarity on legal consequences", 52.52),
    ("Data protection / privacy concerns",    48.83),
    ("Data quality or availability",          44.37),
    ("Incompatibility with existing systems", 41.39),
    ("Cost too high",                         33.34),
    ("Ethical considerations",                23.53),
    ("Not useful for our enterprise",         20.68),
]
labels = [b[0] for b in barriers][::-1]
values = [b[1] for b in barriers][::-1]
colors = [HIGHLIGHT if v == 70.89 else ("#F4A23E" if v == 33.34 else MUTED) for v in values]

fig, ax = plt.subplots(figsize=(11, 7.5), dpi=200)
fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
fig.subplots_adjust(left=0.30, right=0.96, top=0.80, bottom=0.16)

bars = ax.barh(labels, values, color=colors, edgecolor="none", height=0.72)
for bar, v, l in zip(bars, values, labels):
    is_top = (v == 70.89)
    is_cost = (l == "Cost too high")
    color = HIGHLIGHT if is_top else ("#F4A23E" if is_cost else INK)
    weight = "bold" if (is_top or is_cost) else "normal"
    ax.text(v + 1, bar.get_y() + bar.get_height()/2, f"{v:.1f}%",
            va="center", ha="left", fontsize=11.5,
            color=color, fontweight=weight)

cost_y_idx = labels.index("Cost too high")
ax.annotate("Cost ranks 6th — 37 points\nbehind 'lack of expertise'",
            xy=(33.34, cost_y_idx), xytext=(50, cost_y_idx - 1.7),
            fontsize=10.5, color="#B8650A", fontweight="bold",
            ha="left", va="center",
            arrowprops=dict(arrowstyle="->", color="#F4A23E", lw=1.5,
                            connectionstyle="arc3,rad=-0.2"))

ax.set_xlim(0, 92)
ax.set_xlabel("Share of enterprises citing this reason  (%)",
              fontsize=10.5, color="#444", labelpad=10)

add_titles(fig,
           "Why EU companies don't adopt AI — the real reasons",
           "Among EU enterprises that CONSIDERED adopting AI in 2024, the % citing each reason for not going through with it.")
add_footer(fig,
           "Source: Eurostat — isoc_eb_ai, 2024 reference year, published 2026-02-27.\n"
           "Base: EU27 enterprises with ≥10 employees that considered using AI (PC_ENT_AI_EC). Respondents could cite multiple reasons.")
plt.savefig(os.path.join(CHARTS_DIR, "chart_barriers.png"), dpi=200, facecolor=BG)
print("Saved charts/chart_barriers.png"); plt.close()


# ===================================================================
# CHART 2 — Size gap dumbbell
# ===================================================================
df_gap = pd.read_csv(os.path.join(DATA_DIR, "ai_adoption_country_size_gap.csv"))
df_gap = df_gap.dropna(subset=["small_10_49", "large_250plus"]).copy()
df_gap = df_gap.sort_values("small_10_49", ascending=True).reset_index(drop=True)
HILITE = {"Spain": HIGHLIGHT, "France": "#F39C12"}

fig, ax = plt.subplots(figsize=(11, 12), dpi=200)
fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
fig.subplots_adjust(left=0.22, right=0.96, top=0.90, bottom=0.10)

y = np.arange(len(df_gap))
for i, row in df_gap.iterrows():
    color_lbl = HILITE.get(row["geo_label"])
    line_color = color_lbl if color_lbl else "#C8CDD3"
    dot_small = color_lbl if color_lbl else "#6B7280"
    dot_large = color_lbl if color_lbl else INK
    ax.hlines(i, row["small_10_49"], row["large_250plus"],
              color=line_color, linewidth=2.6, alpha=0.85, zorder=1)
    ax.scatter(row["small_10_49"], i, s=80, color=dot_small, zorder=2,
               edgecolor="white", linewidth=1)
    ax.scatter(row["large_250plus"], i, s=130, color=dot_large, zorder=3,
               edgecolor="white", linewidth=1)

display_labels = [
    lbl.replace("European Union - 27 countries (from 2020)", "EU27")
       .replace("Bosnia and Herzegovina", "Bosnia & Herz.")
    for lbl in df_gap["geo_label"]
]
ax.set_yticks(y)
ax.set_yticklabels(display_labels, fontsize=10)
for tick, lbl in zip(ax.get_yticklabels(), df_gap["geo_label"]):
    if lbl in HILITE:
        tick.set_color(HILITE[lbl]); tick.set_fontweight("bold")

spain_idx = df_gap.index[df_gap["geo_label"] == "Spain"].tolist()
if spain_idx:
    si = spain_idx[0]
    ax.annotate(f"Spain: 5.1× gap\n(8.6% small → 44.0% large)",
                xy=(43.96, si), xytext=(54, si + 1.5),
                fontsize=10.5, color=HIGHLIGHT, fontweight="bold",
                ha="left", va="center",
                arrowprops=dict(arrowstyle="->", color=HIGHLIGHT, lw=1.4,
                                connectionstyle="arc3,rad=0.2"))

ax.set_xlim(0, 80)
ax.set_xlabel("Share of enterprises using at least one AI technology  (%)",
              fontsize=10.5, color="#444", labelpad=10)

small_dot = mpatches.Patch(color="#6B7280", label="Small (10–49 employees)")
large_dot = mpatches.Patch(color=INK,       label="Large (250+ employees)")
ax.legend(handles=[small_dot, large_dot], loc="lower right",
          frameon=False, fontsize=10.5)

add_titles(fig,
           "The bigger the company, the more AI it uses",
           "Gap between small (10–49 employees) and large (250+) in each country — 2024, 32 countries.")
add_footer(fig,
           "Source: Eurostat — isoc_eb_ai, 2024 reference year, published 2026-02-27.\n"
           "Indicator E_AI_TANY (uses at least one AI tech), unit PC_ENT (% of enterprises in each size class).")
plt.savefig(os.path.join(CHARTS_DIR, "chart_size_gap.png"), dpi=200, facecolor=BG)
print("Saved charts/chart_size_gap.png"); plt.close()


# ===================================================================
# CHART 3 — GenAI reality
# ===================================================================
genai = [
    ("ML / deep learning",   4.24),
    ("Image recognition",    3.23),
    ("Speech recognition",   4.78),
    ("Text mining (NLP)",    6.88),
    ("GenAI text/code",      5.41),
    ("Workflow automation",  4.19),
]
genai = sorted(genai, key=lambda x: x[1])
labels3 = [b[0] for b in genai]
values3 = [b[1] for b in genai]
colors3 = [HIGHLIGHT if "GenAI" in l else MUTED for l in labels3]

fig, ax = plt.subplots(figsize=(11, 6.5), dpi=200)
fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
fig.subplots_adjust(left=0.22, right=0.96, top=0.78, bottom=0.20)

bars = ax.barh(labels3, values3, color=colors3, edgecolor="none", height=0.65)
for bar, v, l in zip(bars, values3, labels3):
    ax.text(v + 0.15, bar.get_y() + bar.get_height()/2, f"{v:.2f}%",
            va="center", ha="left", fontsize=11.5,
            color=HIGHLIGHT if "GenAI" in l else INK,
            fontweight="bold" if "GenAI" in l else "normal")

genai_idx = labels3.index("GenAI text/code")
ax.annotate("ChatGPT launched\nNov 2022. 41 months later:\n1 in 20 EU enterprises.",
            xy=(5.41, genai_idx), xytext=(6.8, genai_idx - 1.3),
            fontsize=10.5, color=HIGHLIGHT, fontweight="bold",
            ha="left", va="center",
            arrowprops=dict(arrowstyle="->", color=HIGHLIGHT, lw=1.4,
                            connectionstyle="arc3,rad=-0.2"))

ax.set_xlim(0, 11)
ax.set_xlabel("Share of EU enterprises (10+ employees) using this technology in 2024  (%)",
              fontsize=10.5, color="#444", labelpad=10)

add_titles(fig,
           "GenAI is mainstream on LinkedIn. Not in EU production.",
           "Share of EU27 enterprises (10+ employees) using each AI technology in production in 2024.")
add_footer(fig,
           "Source: Eurostat — isoc_eb_ai, 2024 reference year, published 2026-02-27.\n"
           "Indicators E_AI_TML, E_AI_TIR, E_AI_TSR, E_AI_TTM, E_AI_TNLG, E_AI_TPA. Unit PC_ENT (% of all EU27 enterprises in size class).")
plt.savefig(os.path.join(CHARTS_DIR, "chart_genai_reality.png"), dpi=200, facecolor=BG)
print("Saved charts/chart_genai_reality.png"); plt.close()

"""
Build three charts (PNGs in charts/):

  chart_barriers.png      ── Why EU enterprises don't adopt AI
  chart_size_gap.png      ── AI adoption: small vs large by country
  chart_genai_reality.png ── EU GenAI use in production

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
    fig.text(0.06, 0.965, title, fontsize=17, fontweight="bold", color=INK, ha="left", va="top")
    fig.text(0.06, 0.918, subtitle, fontsize=11.5, color="#444", style="italic", ha="left", va="top")


def add_footer(fig, source, credit="Chart by Santiago Patiño Serna"):
    fig.text(0.06, 0.02, source, fontsize=8.5, color="#666", ha="left", va="bottom", linespacing=1.5)
    fig.text(0.98, 0.02, credit, fontsize=8.5, color="#666", ha="right", va="bottom")


# ---------- CHART 1: barriers ----------
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
colors = [HIGHLIGHT if v == 70.89 else MUTED for v in values]

fig, ax = plt.subplots(figsize=(10.5, 7.2), dpi=200)
fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
fig.subplots_adjust(left=0.30, right=0.96, top=0.84, bottom=0.14)

bars = ax.barh(labels, values, color=colors, edgecolor="none", height=0.72)
for bar, v in zip(bars, values):
    ax.text(v + 1, bar.get_y() + bar.get_height()/2, f"{v:.1f}%",
            va="center", ha="left", fontsize=11,
            color=HIGHLIGHT if v == 70.89 else INK,
            fontweight="bold" if v == 70.89 else "normal")
ax.set_xlim(0, 82)
ax.set_xlabel("% of EU enterprises (that considered AI) citing this barrier",
              fontsize=10, color="#555", labelpad=10)
add_titles(fig,
           "Why EU companies don't adopt AI",
           "It's not cost. It's people who can ship it.")
add_footer(fig,
           "Source: Eurostat — isoc_eb_ai, 2024 reference year, published 2026-02-27.\n"
           "Base: EU27 enterprises with ≥10 employees that ever considered using AI (PC_ENT_AI_EC).")
plt.savefig(os.path.join(CHARTS_DIR, "chart_barriers.png"), dpi=200, facecolor=BG)
print("Saved charts/chart_barriers.png"); plt.close()


# ---------- CHART 2: small vs large dumbbell ----------
df_gap = pd.read_csv(os.path.join(DATA_DIR, "ai_adoption_country_size_gap.csv"))
df_gap = df_gap.dropna(subset=["small_10_49", "large_250plus"]).copy()
df_gap = df_gap.sort_values("small_10_49", ascending=True).reset_index(drop=True)
HILITE = {"Spain": HIGHLIGHT, "France": "#F39C12"}

fig, ax = plt.subplots(figsize=(10.5, 11.5), dpi=200)
fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
fig.subplots_adjust(left=0.22, right=0.96, top=0.92, bottom=0.08)

y = np.arange(len(df_gap))
for i, row in df_gap.iterrows():
    color_lbl = HILITE.get(row["geo_label"])
    line_color = color_lbl if color_lbl else "#C8CDD3"
    dot_small = color_lbl if color_lbl else "#6B7280"
    dot_large = color_lbl if color_lbl else INK
    ax.hlines(i, row["small_10_49"], row["large_250plus"],
              color=line_color, linewidth=2.4, alpha=0.85, zorder=1)
    ax.scatter(row["small_10_49"], i, s=70, color=dot_small, zorder=2,
               edgecolor="white", linewidth=0.8)
    ax.scatter(row["large_250plus"], i, s=110, color=dot_large, zorder=3,
               edgecolor="white", linewidth=0.8)

display_labels = [
    lbl.replace("European Union - 27 countries (from 2020)", "EU27")
       .replace("Bosnia and Herzegovina", "Bosnia & Herz.")
    for lbl in df_gap["geo_label"]
]
ax.set_yticks(y)
ax.set_yticklabels(display_labels, fontsize=9.5)
for tick, lbl in zip(ax.get_yticklabels(), df_gap["geo_label"]):
    if lbl in HILITE:
        tick.set_color(HILITE[lbl]); tick.set_fontweight("bold")
ax.set_xlim(0, 75)
ax.set_xlabel("% of enterprises using at least one AI technology, 2024",
              fontsize=10, color="#555", labelpad=10)
small_dot = mpatches.Patch(color="#6B7280", label="Small (10–49 employees)")
large_dot = mpatches.Patch(color=INK,       label="Large (250+ employees)")
ax.legend(handles=[small_dot, large_dot], loc="lower right",
          frameon=False, fontsize=10)
add_titles(fig,
           "The AI mid-market gap is structural, not cultural",
           "Small enterprises (10–49) vs large (250+) — 32 European countries, 2024")
add_footer(fig,
           "Source: Eurostat — isoc_eb_ai, 2024 reference year, published 2026-02-27.\n"
           "Indicator E_AI_TANY, unit PC_ENT (% of enterprises in size class).")
plt.savefig(os.path.join(CHARTS_DIR, "chart_size_gap.png"), dpi=200, facecolor=BG)
print("Saved charts/chart_size_gap.png"); plt.close()


# ---------- CHART 3: GenAI reality ----------
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

fig, ax = plt.subplots(figsize=(10.5, 6), dpi=200)
fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
fig.subplots_adjust(left=0.22, right=0.96, top=0.82, bottom=0.20)

bars = ax.barh(labels3, values3, color=colors3, edgecolor="none", height=0.65)
for bar, v, l in zip(bars, values3, labels3):
    ax.text(v + 0.15, bar.get_y() + bar.get_height()/2, f"{v:.2f}%",
            va="center", ha="left", fontsize=11,
            color=HIGHLIGHT if "GenAI" in l else INK,
            fontweight="bold" if "GenAI" in l else "normal")
ax.set_xlim(0, 9)
ax.set_xlabel("% of EU27 enterprises (10+ employees) using this AI technology, 2024",
              fontsize=10, color="#555", labelpad=10)
add_titles(fig,
           "GenAI is mainstream on LinkedIn. Not in EU production.",
           "Only 5.41% of EU enterprises generate text or code with AI. ChatGPT shipped in 2022.")
add_footer(fig,
           "Source: Eurostat — isoc_eb_ai, 2024 reference year, published 2026-02-27.\n"
           "Indicators E_AI_TML, E_AI_TIR, E_AI_TSR, E_AI_TTM, E_AI_TNLG, E_AI_TPA. PC_ENT base.")
plt.savefig(os.path.join(CHARTS_DIR, "chart_genai_reality.png"), dpi=200, facecolor=BG)
print("Saved charts/chart_genai_reality.png"); plt.close()

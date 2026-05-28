"""
Analyze Eurostat AI-in-enterprises dataset (reference year 2024,
published 2026-02-27).

Run from repo root:  python scripts/analyze.py

Outputs three CSVs in data/:
  ai_tany_all.csv                    — country × size × AI use
  ai_adoption_country_size_gap.csv   — gap analysis
  ai_small_enterprises_country.csv   — small-enterprise ranking
"""
import json, os, itertools
import pandas as pd

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(REPO_ROOT, "data")

RAW = json.load(open(os.path.join(DATA_DIR, "eurostat_isoc_eb_ai_raw.json")))
dim_ids = RAW["id"]
sizes = RAW["size"]
dims = {d: RAW["dimension"][d] for d in dim_ids}

def codes_in_order(dim):
    idx = dim["category"]["index"]
    return sorted(idx.keys(), key=lambda k: idx[k])

dim_codes = {d: codes_in_order(dims[d]) for d in dim_ids}
dim_labels = {d: dims[d]["category"]["label"] for d in dim_ids}

rows = []
for combo in itertools.product(*[range(s) for s in sizes]):
    flat = 0
    stride = 1
    for j in reversed(range(len(sizes))):
        flat += combo[j] * stride
        stride *= sizes[j]
    v = RAW["value"].get(str(flat))
    if v is None:
        continue
    rows.append({dim_ids[j]: dim_codes[dim_ids[j]][combo[j]] for j in range(len(sizes))} | {"value": v})
df = pd.DataFrame(rows)
df["geo_label"] = df["geo"].map(dim_labels["geo"])
df["size_label"] = df["size_emp"].map(dim_labels["size_emp"])
df["indic_label"] = df["indic_is"].map(dim_labels["indic_is"])
print("Long df shape:", df.shape)

head = df[(df["indic_is"] == "E_AI_TANY") & (df["unit"] == "PC_ENT")].copy()
head.to_csv(os.path.join(DATA_DIR, "ai_tany_all.csv"), index=False)

eu = head[head["geo"] == "EU27_2020"].sort_values("size_emp")
print("\n--- EU27 by size, % using ≥1 AI tech ---")
print(eu[["size_emp", "size_label", "value"]].to_string(index=False))

COUNTRY = [g for g in head["geo"].unique() if not g.startswith(("EU", "EA"))]
ctry_ge10 = head[head["geo"].isin(COUNTRY) & (head["size_emp"] == "GE10")].sort_values("value", ascending=False)
print("\n--- Country ranking (10+ employees) ---")
print(ctry_ge10[["geo_label", "value"]].to_string(index=False))

piv = head[head["geo"].isin(COUNTRY)].pivot_table(
    index="geo_label", columns="size_emp", values="value", aggfunc="first"
).rename(columns={"10-49": "small_10_49", "50-249": "mid_50_249",
                  "GE250": "large_250plus", "GE10": "all_10plus"})
piv["gap_large_minus_small"] = piv["large_250plus"] - piv["small_10_49"]
piv["large_over_small_ratio"] = (piv["large_250plus"] / piv["small_10_49"]).round(2)
piv = piv[["small_10_49", "mid_50_249", "large_250plus", "all_10plus",
           "gap_large_minus_small", "large_over_small_ratio"]].sort_values(
    "gap_large_minus_small", ascending=False)
piv.to_csv(os.path.join(DATA_DIR, "ai_adoption_country_size_gap.csv"))

print("\n--- EU27 barriers, % of enterprises that considered AI ---")
barriers = ["E_AI_BLE", "E_AI_BLEG", "E_AI_BCDP", "E_AI_BDDT",
            "E_AI_BINC", "E_AI_BCST", "E_AI_BEC", "E_AI_BNU"]
bar_eu = df[(df["geo"] == "EU27_2020") & (df["indic_is"].isin(barriers))
            & (df["unit"] == "PC_ENT_AI_EC") & (df["size_emp"] == "GE10")]
print(bar_eu[["indic_label", "value"]].sort_values("value", ascending=False).to_string(index=False))

print("\n--- EU27 AI tech breakdown, % all enterprises (10+) ---")
techs = ["E_AI_TANY", "E_AI_TTM", "E_AI_TSR", "E_AI_TNLG", "E_AI_TIR",
         "E_AI_TML", "E_AI_TPA", "E_AI_TAR", "E_AI_TPVSG"]
tech_eu = df[(df["geo"] == "EU27_2020") & (df["indic_is"].isin(techs))
             & (df["unit"] == "PC_ENT") & (df["size_emp"] == "GE10")]
print(tech_eu[["indic_label", "value"]].sort_values("value", ascending=False).to_string(index=False))

small_only = head[head["geo"].isin(COUNTRY) & (head["size_emp"] == "10-49")].sort_values("value", ascending=False)
small_only.to_csv(os.path.join(DATA_DIR, "ai_small_enterprises_country.csv"), index=False)

print("\nSaved: ai_tany_all.csv, ai_adoption_country_size_gap.csv, ai_small_enterprises_country.csv")

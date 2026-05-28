"""
Pull Eurostat dataset `isoc_eb_ai` — Artificial Intelligence by size class of enterprise.

Source: https://ec.europa.eu/eurostat/databrowser/view/isoc_eb_ai
API:    https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/isoc_eb_ai

Run from repo root:  python scripts/fetch.py
"""
import json
import os
import urllib.request

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(REPO_ROOT, "data")
os.makedirs(DATA_DIR, exist_ok=True)

URL = ("https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/"
       "isoc_eb_ai?format=JSON&lang=EN&time=2024")

req = urllib.request.Request(URL, headers={
    "User-Agent": "santiago-patino-research/1.0 santiagopatinoserna@gmail.com",
})
with urllib.request.urlopen(req, timeout=60) as r:
    raw = json.loads(r.read().decode())

with open(os.path.join(DATA_DIR, "eurostat_isoc_eb_ai_raw.json"), "w") as f:
    json.dump(raw, f, indent=2)

print("Saved data/eurostat_isoc_eb_ai_raw.json")
print("Dataset label:", raw.get("label"))
print("Last update:", raw.get("updated"))
print("Source:", raw.get("source"))
print("Total cells:", len(raw.get("value", {})))

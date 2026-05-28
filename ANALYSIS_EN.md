# Why EU companies don't adopt AI: it's not cost, it's expertise (Eurostat 2024)

> Eurostat published its 2024 enterprise AI dataset on 2026-02-27. I downloaded the full cube (16,721 cells, 32 European countries, 8 size classes, 63 indicators) and re-ran the cross-tabs. The headline finding contradicts most coverage: cost ranks sixth among barriers (33.34%). Expertise ranks first (70.89%) — a 37-point gap over cost, and an 18-point gap over the next-cited barrier.

## The finding

Across EU27, only **13.48%** of enterprises with 10+ employees used any AI technology in 2024 — three years after ChatGPT shipped. For generative AI specifically (the technology dominating the LinkedIn narrative), the number is **5.41%**.

When Eurostat asked enterprises that *considered* adopting AI why they didn't go through with it, the ranking was unambiguous:

| Rank | Reason | % of enterprises that considered AI |
|---|---|---|
| 1 | Lack of relevant expertise | **70.89%** |
| 2 | Lack of clarity on legal consequences | 52.52% |
| 3 | Data protection / privacy concerns | 48.83% |
| 4 | Data quality or availability | 44.37% |
| 5 | Incompatibility with existing systems | 41.39% |
| 6 | Cost too high | 33.34% |
| 7 | Ethical considerations | 23.53% |
| 8 | Not useful for our enterprise | 20.68% |

Cost is below "data quality." Cost is below "we don't know what the legal consequences are." The dominant constraint on EU AI adoption is not capex. It is human capital.

## The structural gap by company size

The aggregate adoption number hides a more interesting structure. AI adoption scales almost monotonically with company size:

| Company size | EU27 % using ≥1 AI tech, 2024 |
|---|---|
| Small (10–49 employees) | 11.21% |
| Medium (50–249 employees) | 20.97% |
| **Large (250+ employees)** | **41.17%** |
| All 10+ | 13.48% |

That's a **3.7x ratio** between large and small enterprises across the EU. In Spain, the ratio widens to **5.14x** (43.96% of large enterprises adopt vs 8.56% of small ones). In Poland it's **8.38x**.

The same regulatory framework. The same talent market. The same hyperscaler pricing. The gap is not exogenous — it tracks who has the budget to hire a senior ML engineer with end-to-end ownership.

## Country ranking — and the western European laggard

Top 10 countries by share of all enterprises (10+) using at least one AI technology:

| Rank | Country | % using AI (10+ employees) |
|---|---|---|
| 1 | Denmark | 27.58% |
| 2 | Sweden | 25.09% |
| 3 | Belgium | 24.71% |
| 4 | Finland | 24.37% |
| 5 | Luxembourg | 23.73% |
| 6 | Netherlands | 23.06% |
| 7 | Slovenia | 20.89% |
| 8 | Norway | 20.77% |
| 9 | Austria | 20.27% |
| 10 | Germany | 19.75% |
| — | **EU27 average** | **13.48%** |
| 15 | Spain | 11.31% |
| 18 | France | 9.91% |
| 23 | Italy | 8.20% |
| 32 | Romania | 3.07% |

The Nordics and the Benelux lead. The two largest Latin economies of the EU — France and Italy — sit below the EU27 average. France, often portrayed as an AI policy leader, has lower enterprise AI adoption than Slovenia, Norway, or Estonia.

## What this means for a 2026 AI budget

The data inverts the standard procurement conversation. If cost were the binding constraint, vendor consolidation and price negotiation would unlock adoption. The data says they wouldn't — because cost isn't the binding constraint.

The binding constraints, in order:

1. **Internal expertise that can ship.** Someone who can read a use case, choose a model family (Claude / GPT / Gemini / OSS), pick an inference stack, ship to production, and maintain it as the model lineup churns every 6 months. Eurostat measures this gap directly: it's the #1 reason 70.89% of "intended adopters" stalled.

2. **Legal certainty.** The EU AI Act started entering into force in 2024 and its risk-based provisions roll in through 2026–2027. Among enterprises that considered AI, 52.52% pointed to legal uncertainty. The compliance map is now public — the gap is whoever inside the company has read it.

3. **Data foundations.** 44.37% blocked on data quality or availability. AI does not fix data problems; it amplifies them. Most "AI projects" that stall before MVP stall here.

4. **Integration with legacy systems.** 41.39%. The pattern is familiar: vendor demo on greenfield data → POC works → production integration breaks against the actual ERP / CRM / data warehouse.

5. **Cost.** A real constraint, but ranked 6th. Most AI workloads under €5k/month MRR are inference + small storage. The capex shape of AI has shifted from training to operations.

## Recommendation matrix

| If you are… | Then your binding constraint is probably… | What to do first |
|---|---|---|
| A small enterprise (10–49 employees) with no AI in production | Expertise — you can't hire a full-time senior ML engineer at your size | Buy fractional AI leadership 1–2 days/week, run a 30-day audit, ship one production use case, then evaluate. Do NOT start with a vendor demo. |
| A mid-market company (50–249 employees) with one or two AI POCs | Integration + ownership transfer from vendor | Insist on a named internal owner who runs the POC by month 3 without vendor hand-holding. If no candidate exists, the POC will not survive vendor renewal. |
| A large enterprise (250+ employees) with multiple stalled AI initiatives | Legal certainty + data quality | Map your AI Act classification today. Audit one critical data domain (CRM, ERP, support tickets) before greenlighting another POC. |
| A French or Italian mid-market company | All of the above, plus the country-level adoption gap | The competitive cost of not moving is rising. Italian and French mid-market are losing ground to Iberian and Central European peers on AI deployment. |

## What this analysis does NOT measure

- **Quality of deployment.** Eurostat measures "uses at least one AI technology" — it doesn't measure whether the deployment is value-generating, profitable, or even still running.
- **Shadow AI.** Employees using ChatGPT personal accounts at work are invisible to this dataset. Real GenAI exposure is almost certainly higher than 5.41%; *enterprise-sanctioned* GenAI is what the 5.41% captures.
- **Vertical breakdown.** The dataset is cross-sector (NACE excluding agriculture, mining, financial). A retail bank and a manufacturing SME are aggregated.
- **Causation.** The size-gap correlation is structural, not causal. Large enterprises adopt more for many reasons (budget, talent, data maturity, regulatory exposure).

## How I built this analysis

Everything in this article is reproducible in under 5 minutes. The Eurostat REST API is free, no key required.

```python
import urllib.request, json
URL = ("https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/"
       "isoc_eb_ai?format=JSON&lang=EN&time=2024")
raw = json.loads(urllib.request.urlopen(URL).read())
# raw['value'] is a flat dict keyed by the flattened cube index.
# Dimensions in raw['id']: freq, size_emp, nace_r2, indic_is, unit, geo, time.
```

The 16,721 cells were flattened to a long-format DataFrame, then filtered to indicator `E_AI_TANY` (uses at least one AI technology) with unit `PC_ENT` (% of enterprises in the size class). The barrier ranking uses indicators `E_AI_BLE` through `E_AI_BNU` with unit `PC_ENT_AI_EC` (% of enterprises that considered AI).

Full analysis script and CSVs are in the public dataset folder linked at the end.

## Methodology + raw data

- **Source:** Eurostat dataset `isoc_eb_ai` — "Artificial intelligence by size class of enterprise"
- **Reference year:** 2024
- **Publication date:** 2026-02-27
- **Geographic scope:** EU27 + EFTA + selected candidates (32 countries with country-level data)
- **Sector scope:** NACE Rev. 2 sections C10–S95 excluding K (all activities except agriculture, forestry, fishing, mining, and financial sector)
- **Sample:** Enterprises with at least 10 employees, with size breakdowns at 10–49, 50–249, 250+

Bias caveats:
- Self-reported survey, not telemetry — companies may overstate "we use AI" if any employee touches a tool with AI features.
- The 70.89% expertise figure is the share among enterprises *that considered AI* — not the general population.
- "AI" is defined by Eurostat across 8 specific technology categories. Newer paradigms (agentic AI, MCP-based architectures) are not yet disaggregated.

## Next step

If your 2026 AI roadmap is stalled on the #1 barrier — finding someone who can choose, ship, and maintain — book a 15-minute diagnostic. Same data rigor applied to your stack, your data, your constraints. €97.

→ godi.ai/audit-ia-quick
→ santiagopatinoserna@godi.ai

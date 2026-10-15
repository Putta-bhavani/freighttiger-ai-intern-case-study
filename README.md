# FreightTiger Shipping Cost Watch — AI Intern Case Study

## Overview
This project analyzes shipment costs by route and Monday-starting week, compares each week's cost per tonne-km with the route's own trailing history and same-week peer routes, then checks whether a detected increase has a directly applicable explanation in the supplied context notes.

## Run locally
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python analyze.py
streamlit run app.py
pytest -q
```
Input files are in `data/`. The command writes `output.csv`. The Streamlit dashboard offers filters, trend charts, and CSV download.

## Method
1. `route = origin + "-" + destination`; preserve the provided `route_type`.
2. Assign each shipment to the Monday of its Monday–Sunday week.
3. Weekly cost per tonne-km = sum(freight_cost_inr) / sum(quantity_tonnes × distance_km).
4. Own-history baseline = average of the previous up to eight *observed route-week* costs, strictly before the current week. When fewer than eight exist, use all available prior observations; no padding or look-ahead.
5. Peer baseline = average current-week cost per tonne-km for all other routes with the same route_type. Exclude the current route.
6. Percentage comparisons = (current / baseline − 1) × 100. When a baseline is absent or zero, show it as unavailable rather than inventing a value.
7. Threshold policy: flag an increase when either available comparison is at least +20%. The assignment asks for an out-of-ordinary increase but does not prescribe a numerical threshold; +20% is an explicit, configurable policy choice, not a threshold provided by FreightTiger.
8. If flagged, apply deterministic route/date/effect checks to context notes. Only N001 (flooding on Chennai–Bangalore during Feb 24–Mar 8, 2025), N002 (festival surcharge on Ahmedabad–Mumbai during the week of Jan 20, 2025), and N003 (nationwide diesel increase beginning May 5, 2025, only when the historical rise is in a conservative 3–10% band consistent with the note's roughly 5–7% description) can justify an increase. N004 says affected routes are outside this dataset; N005 explicitly says costs were not significantly affected; N006/N008 report no significant disruption; N007 reports improved road conditions; N009 says the flood disruption had ended; N010 says compliance costs did not change rates. Those notes are not accepted as cost-increase justifications.
9. `Yes` = anomaly needing human review without a valid note. `No (justified)` = anomaly with an applicable note. `No` = no baseline comparison crosses the threshold.

## AI / trust design
The brief's AI bonus is evidence retrieval and plain-English explanations, not an obligation to call an LLM for every row. There are only ten supplied notes, so this version uses deterministic, auditable retrieval rules to avoid hallucinated justifications and repeated API cost. It makes no LLM calls: input tokens = 0, output tokens = 0, LLM calls = 0, estimated LLM cost = $0. This is a genuine cost log, not an estimate for an unused model. An optional next step is to add embeddings/LLM wording while keeping verdicts and matched note IDs controlled by the deterministic validation layer.

## Reproducibility and evaluation
Run `python analyze.py --output run1.csv`, `run2.csv`, and `run3.csv`, then compare the files:
```bash
python analyze.py --output run1.csv
python analyze.py --output run2.csv
python analyze.py --output run3.csv
# Windows PowerShell:
Get-FileHash run1.csv,run2.csv,run3.csv -Algorithm SHA256
# macOS/Linux:
sha256sum run1.csv run2.csv run3.csv
```
All numbers, flags, matched note IDs, and reasons are deterministic. Run `pytest -q` for checks covering schema, repeatability, and evidence IDs. The test suite is a lightweight software-quality check; it is not a fully labeled precision/recall benchmark. For a stronger evaluation, manually label a sample of route-week anomalies and report false positives/false negatives.

## Output schema
Exactly these columns, in order:
`route, week_of, cost_per_tonne_km, vs_own_history, vs_similar_routes, flagged, matched_note_id, reason`

## Important limitations / trade-offs
- The 20% threshold is a documented assumption because the brief does not define one. Review sensitivity to 10%, 15%, and 25% before production use.
- Peer comparison is unavailable where there is no other route of the same route_type in the same week.
- The supplied notes are sparse; absence of a note means “unexplained by provided evidence,” not proof of wrongdoing.
- The dashboard is a local demo. Deploy it to Streamlit Community Cloud or another host and verify the public link before submission.
- No LLM is used in this baseline implementation; this avoids hallucinations and API spend, but the optional natural-language Q&A stretch goal is not implemented.

## 10-minute walkthrough
1. Problem and output schema (1 min)
2. Weekly aggregation and formula (2 min)
3. Historical and peer baselines (2 min)
4. Context-note validation and example (2 min)
5. Reproducibility tests and cost log (1 min)
6. Dashboard demo, limitations, next steps (2 min)
